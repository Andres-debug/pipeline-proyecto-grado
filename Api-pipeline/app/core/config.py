from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


load_dotenv()


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


def _resolve_path(base: Path, value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else (base / path).resolve()


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
    )


settings = get_settings()
