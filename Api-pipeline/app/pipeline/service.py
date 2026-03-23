from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from app.core.config import settings
from app.db.load import load_star_to_postgres
from app.db.service import is_database_configured
from app.pipeline.cleaning import clean_dataset
from app.pipeline.io import load_mapping, map_columns, read_flexible_file
from app.pipeline.modeling import (
    build_dim_geografia,
    build_dim_tiempo,
    build_dim_tipo_movilidad,
    build_dim_universidad,
    build_fact_movilidad,
    build_kpis,
)
from app.pipeline.synthetic import save_synthetic_data

logger = logging.getLogger(__name__)


@dataclass
class PipelineRunResult:
    rows_consolidated: int
    output_files: dict[str, str]
    dimensions: dict[str, int]
    kpis_total: int
    warnings: list[str]


class PipelineService:
    def __init__(self) -> None:
        self.last_status: dict = {
            "last_run_at": None,
            "status": "idle",
            "details": {},
        }

    def _ensure_directories(self) -> None:
        settings.raw_dir.mkdir(parents=True, exist_ok=True)
        settings.processed_dir.mkdir(parents=True, exist_ok=True)
        settings.results_dir.mkdir(parents=True, exist_ok=True)
        settings.reports_dir.mkdir(parents=True, exist_ok=True)

    def generate_synthetic(
        self,
        rows: int = 2000,
        university: str = "Tecnológico de Antioquia",
        year_start: int = 2022,
        year_end: int = 2026,
        seed: int = 42,
        file_stem: str | None = None,
    ) -> dict[str, str | int]:
        self._ensure_directories()

        if year_start > year_end:
            raise ValueError("year_start no puede ser mayor que year_end")

        output_path = save_synthetic_data(
            output_dir=settings.raw_dir,
            rows=rows,
            university=university,
            year_start=year_start,
            year_end=year_end,
            seed=seed,
            file_stem=file_stem,
        )

        return {
            "file_path": str(output_path),
            "rows_generated": rows,
        }

    def _load_source(self, path: Path, source_key: str, display_name: str, mapping_cfg: dict) -> tuple[pd.DataFrame | None, str | None]:
        if not path.exists():
            return None, f"No se encontró la fuente {display_name}: {path}"

        raw_df = read_flexible_file(path)
        canonical_columns: list[str] = mapping_cfg["canonical_columns"]
        source_map: dict = mapping_cfg["sources"]
        mapped_df = map_columns(raw_df, source_key, canonical_columns, source_map)
        university_override = self._guess_university_override(path)
        if university_override:
            mapped_df["UNIVERSIDAD"] = university_override
        else:
            mapped_df["UNIVERSIDAD"] = mapped_df["UNIVERSIDAD"].fillna(display_name)
        return mapped_df, None

    @staticmethod
    def _guess_university_override(file_path: Path) -> str | None:
        file_name = file_path.name.lower()
        if "registro de movilidades" in file_name:
            return "Tecnológico de Antioquia"
        return None

    @staticmethod
    def _guess_is_synthetic(file_path: Path) -> int:
        file_name = file_path.name.lower()
        synthetic_markers = ["sintet", "synthetic", "mock", "fake", "demo"]
        return 1 if any(marker in file_name for marker in synthetic_markers) else 0

    @staticmethod
    def _guess_source_key(file_path: Path) -> str:
        file_name = file_path.name.lower()
        if "docente" in file_name:
            return "docentes_exterior"
        return "iush"

    @staticmethod
    def _supported_input_files(raw_dir: Path) -> list[Path]:
        allowed_suffixes = {".csv", ".xlsx", ".xls", ".json"}
        return sorted(
            [
                path
                for path in raw_dir.iterdir()
                if path.is_file()
                and path.suffix.lower() in allowed_suffixes
                and not path.name.startswith("~$")
            ],
            key=lambda file_path: file_path.name.lower(),
        )

    def _resolve_sources(
        self,
        iush_filename: str | None,
        docentes_filename: str | None,
        input_files: list[str] | None,
        auto_discover: bool,
    ) -> list[Path]:
        if input_files:
            return [settings.raw_dir / file_name for file_name in input_files]

        if iush_filename or docentes_filename:
            selected: list[Path] = []
            if iush_filename:
                selected.append(settings.raw_dir / iush_filename)
            if docentes_filename:
                selected.append(settings.raw_dir / docentes_filename)
            return selected

        if auto_discover:
            return self._supported_input_files(settings.raw_dir)

        return []

    def run(
        self,
        iush_filename: str | None = None,
        docentes_filename: str | None = None,
        input_files: list[str] | None = None,
        auto_discover: bool = True,
    ) -> PipelineRunResult:
        self.last_status = {
            "last_run_at": datetime.now(timezone.utc),
            "status": "running",
            "details": {},
        }

        try:
            self._ensure_directories()
            mapping_cfg = load_mapping(settings.column_mapping_path)

            source_paths = self._resolve_sources(
                iush_filename=iush_filename,
                docentes_filename=docentes_filename,
                input_files=input_files,
                auto_discover=auto_discover,
            )
            if not source_paths:
                raise ValueError("No se encontraron fuentes para procesar en data/raw.")

            warnings: list[str] = []
            frames: list[pd.DataFrame] = []
            loaded_files: list[str] = []

            for source_path in source_paths:
                source_key = self._guess_source_key(source_path)
                display_name = source_path.stem.upper()
                source_df, source_warning = self._load_source(source_path, source_key, display_name, mapping_cfg)
                if source_warning:
                    warnings.append(source_warning)
                    continue
                if source_df is not None:
                    source_df["ES_SINTETICO"] = self._guess_is_synthetic(source_path)
                    frames.append(source_df)
                    loaded_files.append(source_path.name)

            if not frames:
                raise ValueError("No se pudo cargar ninguna fuente. Revisa archivos en data/raw.")

            consolidated_df = pd.concat(frames, ignore_index=True)
            consolidated_df = clean_dataset(consolidated_df)

            cleaned_output = settings.processed_dir / "datos_consolidados_limpios.csv"
            consolidated_df.to_csv(cleaned_output, index=False, encoding="utf-8")

            dim_tiempo = build_dim_tiempo(consolidated_df)
            dim_geografia = build_dim_geografia(consolidated_df)
            dim_universidad = build_dim_universidad(consolidated_df)
            dim_tipo_movilidad = build_dim_tipo_movilidad(consolidated_df)
            fact_movilidad = build_fact_movilidad(
                consolidated_df,
                dim_tiempo,
                dim_geografia,
                dim_universidad,
                dim_tipo_movilidad,
            )
            kpis = build_kpis(consolidated_df)

            output_files = {
                "datos_consolidados": str(cleaned_output),
                "dim_tiempo": str(settings.results_dir / "dim_tiempo.csv"),
                "dim_geografia": str(settings.results_dir / "dim_geografia.csv"),
                "dim_universidad": str(settings.results_dir / "dim_universidad.csv"),
                "dim_tipo_movilidad": str(settings.results_dir / "dim_tipo_movilidad.csv"),
                "fact_movilidad": str(settings.results_dir / "fact_movilidad.csv"),
                "kpis": str(settings.results_dir / "kpis_powerbi.csv"),
                "datos_completos_powerbi": str(settings.results_dir / "datos_completos_powerbi.csv"),
            }

            dim_tiempo.to_csv(output_files["dim_tiempo"], index=False)
            dim_geografia.to_csv(output_files["dim_geografia"], index=False)
            dim_universidad.to_csv(output_files["dim_universidad"], index=False)
            dim_tipo_movilidad.to_csv(output_files["dim_tipo_movilidad"], index=False)
            fact_movilidad.to_csv(output_files["fact_movilidad"], index=False)
            kpis.to_csv(output_files["kpis"], index=False)
            consolidated_df.to_csv(output_files["datos_completos_powerbi"], index=False)

            db_tables: dict[str, str] = {}
            if is_database_configured(settings.db_url):
                db_tables = load_star_to_postgres(
                    dim_tiempo=dim_tiempo,
                    dim_geografia=dim_geografia,
                    dim_universidad=dim_universidad,
                    dim_tipo_movilidad=dim_tipo_movilidad,
                    fact_movilidad=fact_movilidad,
                    kpis=kpis,
                )
            else:
                warnings.append("DB_URL no configurado. Se omitió la carga en PostgreSQL.")

            report_path = settings.reports_dir / "reporte_calidad_datos_api.txt"
            report_lines = [
                "REPORTE DE EJECUCIÓN PIPELINE API",
                f"Fecha UTC: {datetime.now(timezone.utc).isoformat()}",
                f"Archivos cargados: {', '.join(loaded_files) if loaded_files else 'Ninguno'}",
                f"Registros consolidados: {len(consolidated_df)}",
                f"Dimensión tiempo: {len(dim_tiempo)}",
                f"Dimensión geografía: {len(dim_geografia)}",
                f"Dimensión universidad: {len(dim_universidad)}",
                f"Dimensión tipo movilidad: {len(dim_tipo_movilidad)}",
                f"Tabla de hechos: {len(fact_movilidad)}",
                f"KPIs: {len(kpis)}",
            ]
            if warnings:
                report_lines.extend(["Advertencias:"] + [f"- {warning}" for warning in warnings])
            if db_tables:
                report_lines.extend(["Tablas cargadas en PostgreSQL:"] + [f"- {name}: {table}" for name, table in db_tables.items()])
            report_path.write_text("\n".join(report_lines), encoding="utf-8")
            output_files["reporte"] = str(report_path)

            run_result = PipelineRunResult(
                rows_consolidated=len(consolidated_df),
                output_files=output_files,
                dimensions={
                    "dim_tiempo": len(dim_tiempo),
                    "dim_geografia": len(dim_geografia),
                    "dim_universidad": len(dim_universidad),
                    "dim_tipo_movilidad": len(dim_tipo_movilidad),
                    "fact_movilidad": len(fact_movilidad),
                },
                kpis_total=len(kpis),
                warnings=warnings,
            )

            self.last_status = {
                "last_run_at": datetime.now(timezone.utc),
                "status": "success",
                "details": {
                    "rows_consolidated": run_result.rows_consolidated,
                    "warnings": warnings,
                    "db_tables": db_tables,
                },
            }
            return run_result
        except Exception as error:
            logger.exception("Error ejecutando pipeline")
            self.last_status = {
                "last_run_at": datetime.now(timezone.utc),
                "status": "error",
                "details": {"error": str(error)},
            }
            raise


pipeline_service = PipelineService()
