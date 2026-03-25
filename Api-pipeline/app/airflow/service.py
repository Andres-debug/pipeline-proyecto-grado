from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any

import httpx

from app.core.config import settings


@dataclass
class AirflowClientError(Exception):
    status_code: int
    detail: str


def is_airflow_configured() -> bool:
    return bool(settings.airflow_api_base_url and settings.airflow_api_base_url.strip())


def _build_url(path: str) -> str:
    if not settings.airflow_api_base_url:
        raise AirflowClientError(status_code=400, detail="AIRFLOW_API_BASE_URL no configurado")

    base = settings.airflow_api_base_url.rstrip("/")
    if base.endswith("/api/v1"):
        return f"{base}{path}"
    return f"{base}/api/v1{path}"


def _get_auth() -> tuple[str, str] | None:
    if settings.airflow_username and settings.airflow_password:
        return (settings.airflow_username, settings.airflow_password)
    return None


def _request(method: str, path: str, *, params: dict[str, Any] | None = None, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    url = _build_url(path)
    auth = _get_auth()

    try:
        with httpx.Client(timeout=settings.airflow_timeout_seconds, verify=settings.airflow_verify_ssl, auth=auth) as client:
            response = client.request(method, url, params=params, json=payload)
            response.raise_for_status()
            if not response.content:
                return {}
            return response.json()
    except httpx.HTTPStatusError as error:
        detail = _extract_error_detail(error.response)
        raise AirflowClientError(status_code=error.response.status_code, detail=detail) from error
    except httpx.HTTPError as error:
        raise AirflowClientError(status_code=502, detail=f"No se pudo conectar con Airflow: {error}") from error


def _extract_error_detail(response: httpx.Response) -> str:
    try:
        payload = response.json()
    except ValueError:
        return response.text or "Error desconocido desde Airflow"

    if isinstance(payload, dict):
        title = str(payload.get("title", "")).strip()
        detail = str(payload.get("detail", "")).strip()
        if title and detail:
            return f"{title}: {detail}"
        if detail:
            return detail
        if title:
            return title
    return str(payload)


def get_health() -> dict[str, Any]:
    return _request("GET", "/health")


def list_dags(limit: int = 25, only_active: bool = True) -> list[dict[str, Any]]:
    payload = _request(
        "GET",
        "/dags",
        params={
            "limit": limit,
            "only_active": str(only_active).lower(),
        },
    )
    dags = payload.get("dags", [])

    simplified: list[dict[str, Any]] = []
    for dag in dags:
        simplified.append(
            {
                "dag_id": dag.get("dag_id"),
                "is_paused": dag.get("is_paused"),
                "is_active": dag.get("is_active"),
                "description": dag.get("description"),
            }
        )
    return simplified


def trigger_dag_run(
    dag_id: str,
    conf: dict[str, Any] | None = None,
    dag_run_id: str | None = None,
    logical_date: datetime | None = None,
) -> dict[str, Any]:
    request_payload: dict[str, Any] = {}
    if conf is not None:
        request_payload["conf"] = conf
    if dag_run_id:
        request_payload["dag_run_id"] = dag_run_id
    if logical_date:
        request_payload["logical_date"] = logical_date.isoformat()

    response = _request("POST", f"/dags/{dag_id}/dagRuns", payload=request_payload)
    return {
        "dag_id": dag_id,
        "dag_run_id": response.get("dag_run_id"),
        "state": response.get("state"),
        "logical_date": response.get("logical_date"),
        "start_date": response.get("start_date"),
        "end_date": response.get("end_date"),
    }


def get_dag_run(dag_id: str, dag_run_id: str) -> dict[str, Any]:
    response = _request("GET", f"/dags/{dag_id}/dagRuns/{dag_run_id}")
    return {
        "dag_id": dag_id,
        "dag_run_id": response.get("dag_run_id"),
        "state": response.get("state"),
        "logical_date": response.get("logical_date"),
        "start_date": response.get("start_date"),
        "end_date": response.get("end_date"),
    }
