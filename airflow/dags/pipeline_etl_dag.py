"""
DAG: pipeline_etl_movilidad
Orquesta el pipeline ETL de movilidad académica:
  1. validate_raw   — verifica que existan archivos CSV/XLSX en data/raw
  2. clean_silver   — limpieza y estandarización de columnas
  3. build_gold     — construcción del modelo estrella (dimensiones + hechos)
  4. load_postgres  — carga en PostgreSQL via la API interna
  5. report         — registra métricas del run en el log de Airflow
"""

from __future__ import annotations

import json
import logging
import os
from datetime import datetime, timedelta
from pathlib import Path

import requests
from airflow import DAG
from airflow.operators.python import PythonOperator

log = logging.getLogger(__name__)

# ── Configuración ──────────────────────────────────────────────────────────────
API_BASE_URL = os.getenv("PIPELINE_API_BASE_URL", "http://api:8000")
RAW_DATA_PATH = Path(os.getenv("RAW_DATA_PATH", "/opt/airflow/data/raw"))

DEFAULT_ARGS = {
    "owner": "travelunidata",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=3),
    "email_on_failure": False,
    "email_on_retry": False,
}


# ── Tareas ─────────────────────────────────────────────────────────────────────

def validate_raw(**context: object) -> dict:
    """Verifica que haya archivos procesables en el directorio raw."""
    extensions = {".csv", ".xlsx", ".xls"}

    if not RAW_DATA_PATH.exists():
        raise FileNotFoundError(
            f"Directorio raw no encontrado: {RAW_DATA_PATH}. "
            "Asegúrate de montar el volumen de datos en el contenedor de Airflow."
        )

    files = [f for f in RAW_DATA_PATH.iterdir() if f.suffix.lower() in extensions]

    if not files:
        raise ValueError(
            f"No se encontraron archivos CSV/XLSX en {RAW_DATA_PATH}. "
            "Sube archivos primero desde el portal o la API."
        )

    log.info("Archivos raw encontrados: %s", [f.name for f in files])
    context["ti"].xcom_push(key="raw_files", value=[str(f) for f in files])
    return {"raw_files": [f.name for f in files]}


def run_pipeline_via_api(**context: object) -> dict:
    """Llama al endpoint de la API para ejecutar el pipeline completo."""
    url = f"{API_BASE_URL}/pipeline/run"

    try:
        response = requests.post(url, json={}, timeout=300)
        response.raise_for_status()
    except requests.exceptions.ConnectionError as exc:
        raise RuntimeError(
            f"No se pudo conectar con la API en {url}. "
            "Verifica que el contenedor 'api' esté corriendo."
        ) from exc
    except requests.exceptions.HTTPError as exc:
        body = {}
        try:
            body = exc.response.json()
        except Exception:
            pass
        raise RuntimeError(
            f"Error HTTP {exc.response.status_code} desde la API: {body.get('detail', exc)}"
        ) from exc

    result = response.json()
    log.info("Pipeline ejecutado exitosamente: %s", json.dumps(result, indent=2, default=str))

    context["ti"].xcom_push(key="pipeline_result", value=result)
    return result


def report_metrics(**context: object) -> None:
    """Lee el resultado del pipeline desde XCom y lo reporta en los logs."""
    ti = context["ti"]
    result = ti.xcom_pull(task_ids="run_pipeline", key="pipeline_result") or {}

    rows = result.get("rows_consolidated", "N/A")
    kpis = result.get("kpis_total", "N/A")
    dimensions = result.get("dimensions", {})
    warnings = result.get("warnings", [])

    log.info("=" * 60)
    log.info("REPORTE PIPELINE ETL — %s", datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC"))
    log.info("  Registros consolidados : %s", rows)
    log.info("  KPIs generados         : %s", kpis)
    log.info("  Dimensiones cargadas   :")
    for dim, count in dimensions.items():
        log.info("    %-25s %s filas", dim, count)
    if warnings:
        log.warning("  Advertencias (%s):", len(warnings))
        for w in warnings:
            log.warning("    - %s", w)
    log.info("=" * 60)


# ── DAG ────────────────────────────────────────────────────────────────────────

with DAG(
    dag_id="pipeline_etl_movilidad",
    description="ETL de movilidad académica: raw → limpieza → star schema → PostgreSQL",
    default_args=DEFAULT_ARGS,
    start_date=datetime(2026, 1, 1),
    schedule=None,          # Ejecución manual o via API; cambiar a "0 6 * * 1" para cada lunes
    catchup=False,
    tags=["etl", "movilidad", "travelunidata"],
    max_active_runs=1,
) as dag:

    t1_validate = PythonOperator(
        task_id="validate_raw",
        python_callable=validate_raw,
    )

    t2_run_pipeline = PythonOperator(
        task_id="run_pipeline",
        python_callable=run_pipeline_via_api,
    )

    t3_report = PythonOperator(
        task_id="report_metrics",
        python_callable=report_metrics,
    )

    t1_validate >> t2_run_pipeline >> t3_report
