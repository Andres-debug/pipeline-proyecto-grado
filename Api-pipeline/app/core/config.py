from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


PROJECT_DIR = Path(__file__).resolve().parents[2]
ENV_PATH = PROJECT_DIR / ".env"
load_dotenv(dotenv_path=ENV_PATH)


@dataclass(frozen=True)
class Settings:
    app_name: str
    app_env: str
    app_host: str
    app_port: int
    project_dir: Path
    data_base_dir: Path
    raw_dir: Path
    processed_dir: Path
    results_dir: Path
    reports_dir: Path
    column_mapping_path: Path
    db_url: str | None
    db_schema: str
    airflow_api_base_url: str | None
    airflow_username: str | None
    airflow_password: str | None
    airflow_timeout_seconds: int
    airflow_verify_ssl: bool


def _resolve_path(base: Path, value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else (base / path).resolve()


def _get_bool_env(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def get_settings() -> Settings:
    project_dir = Path(__file__).resolve().parents[2]

    app_name = os.getenv("APP_NAME", "API Pipeline Turismo Academico")
    app_env = os.getenv("APP_ENV", "dev")
    app_host = os.getenv("APP_HOST", "127.0.0.1")
    app_port = int(os.getenv("APP_PORT", "8000"))

    data_base = _resolve_path(project_dir, os.getenv("DATA_BASE_DIR", ".."))
    raw_dir = _resolve_path(data_base, os.getenv("RAW_DIR", "data/raw"))
    processed_dir = _resolve_path(data_base, os.getenv("PROCESSED_DIR", "data/processed"))
    results_dir = _resolve_path(data_base, os.getenv("RESULTS_DIR", "data/results"))
    reports_dir = _resolve_path(data_base, os.getenv("REPORTS_DIR", "outputs/reportes"))

    mapping_value = os.getenv("COLUMN_MAPPING_PATH", "config/column_mappings.json")
    column_mapping_path = _resolve_path(project_dir, mapping_value)

    db_url = os.getenv("DB_URL") or None
    db_schema = os.getenv("DB_SCHEMA", "public")
    airflow_api_base_url = os.getenv("AIRFLOW_API_BASE_URL") or None
    airflow_username = os.getenv("AIRFLOW_USERNAME") or None
    airflow_password = os.getenv("AIRFLOW_PASSWORD") or None
    airflow_timeout_seconds = int(os.getenv("AIRFLOW_TIMEOUT_SECONDS", "30"))
    airflow_verify_ssl = _get_bool_env("AIRFLOW_VERIFY_SSL", True)

    return Settings(
        app_name=app_name,
        app_env=app_env,
        app_host=app_host,
        app_port=app_port,
        project_dir=project_dir,
        data_base_dir=data_base,
        raw_dir=raw_dir,
        processed_dir=processed_dir,
        results_dir=results_dir,
        reports_dir=reports_dir,
        column_mapping_path=column_mapping_path,
        db_url=db_url,
        db_schema=db_schema,
        airflow_api_base_url=airflow_api_base_url,
        airflow_username=airflow_username,
        airflow_password=airflow_password,
        airflow_timeout_seconds=airflow_timeout_seconds,
        airflow_verify_ssl=airflow_verify_ssl,
    )


settings = get_settings()
