from __future__ import annotations

from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, HTTPException
from fastapi import File, UploadFile

from app.airflow.service import (
    AirflowClientError,
    get_dag_run,
    get_health,
    is_airflow_configured,
    list_dags,
    trigger_dag_run,
)
from app.core.config import settings
from app.pipeline.service import pipeline_service
from app.schemas import (
    AirflowDagsResponse,
    AirflowDagRunResponse,
    AirflowHealthResponse,
    GenerateSyntheticRequest,
    GenerateSyntheticResponse,
    PipelineStatus,
    RunPipelineRequest,
    RunPipelineResponse,
    TriggerDagRunRequest,
)

router = APIRouter()


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/pipeline/status", response_model=PipelineStatus)
def pipeline_status() -> PipelineStatus:
    return PipelineStatus(**pipeline_service.last_status)


@router.post("/pipeline/run", response_model=RunPipelineResponse)
def run_pipeline(payload: RunPipelineRequest) -> RunPipelineResponse:
    try:
        result = pipeline_service.run(
            iush_filename=payload.iush_filename,
            docentes_filename=payload.docentes_filename,
            input_files=payload.input_files,
            auto_discover=payload.auto_discover,
        )
        return RunPipelineResponse(
            status="success",
            message="Pipeline ejecutado correctamente",
            rows_consolidated=result.rows_consolidated,
            output_files=result.output_files,
            dimensions=result.dimensions,
            kpis_total=result.kpis_total,
            warnings=result.warnings,
        )
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error)) from error


@router.post("/pipeline/upload-run", response_model=RunPipelineResponse)
def upload_and_run_pipeline(files: list[UploadFile] = File(...)) -> RunPipelineResponse:
    allowed_suffixes = {".csv", ".xlsx", ".xls", ".json"}
    saved_files: list[str] = []

    try:
        settings.raw_dir.mkdir(parents=True, exist_ok=True)

        for upload in files:
            if not upload.filename:
                raise HTTPException(status_code=400, detail="Se recibió un archivo sin nombre.")

            suffix = Path(upload.filename).suffix.lower()
            if suffix not in allowed_suffixes:
                raise HTTPException(
                    status_code=400,
                    detail=f"Formato no soportado: {upload.filename}. Solo CSV, XLS, XLSX o JSON.",
                )

            safe_name = Path(upload.filename).name.replace(" ", "_")
            target_name = f"upload_{uuid4().hex}_{safe_name}"
            target_path = settings.raw_dir / target_name

            content = upload.file.read()
            if not content:
                raise HTTPException(status_code=400, detail=f"El archivo {upload.filename} está vacío.")

            target_path.write_bytes(content)
            saved_files.append(target_name)

        result = pipeline_service.run(input_files=saved_files, auto_discover=False)
        warnings = list(result.warnings)
        warnings.append(f"Archivos cargados por API: {', '.join(saved_files)}")

        return RunPipelineResponse(
            status="success",
            message="Archivos cargados y pipeline ejecutado correctamente",
            rows_consolidated=result.rows_consolidated,
            output_files=result.output_files,
            dimensions=result.dimensions,
            kpis_total=result.kpis_total,
            warnings=warnings,
        )
    except HTTPException:
        raise
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error)) from error
    finally:
        for upload in files:
            upload.file.close()


@router.post("/pipeline/generate-synthetic", response_model=GenerateSyntheticResponse)
def generate_synthetic(payload: GenerateSyntheticRequest) -> GenerateSyntheticResponse:
    try:
        result = pipeline_service.generate_synthetic(
            rows=payload.rows,
            university=payload.university,
            year_start=payload.year_start,
            year_end=payload.year_end,
            seed=payload.seed,
            file_stem=payload.file_stem,
        )
        return GenerateSyntheticResponse(
            status="success",
            message="Archivo sintético generado correctamente",
            file_path=result["file_path"],
            rows_generated=result["rows_generated"],
        )
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error)) from error


@router.get("/airflow/health", response_model=AirflowHealthResponse)
def airflow_health() -> AirflowHealthResponse:
    if not is_airflow_configured():
        return AirflowHealthResponse(
            configured=False,
            status="not_configured",
            detail={"message": "Configura AIRFLOW_API_BASE_URL en .env"},
        )

    try:
        health = get_health()
        return AirflowHealthResponse(configured=True, status="ok", detail=health)
    except AirflowClientError as error:
        raise HTTPException(status_code=error.status_code, detail=error.detail) from error


@router.get("/airflow/dags", response_model=AirflowDagsResponse)
def airflow_list_dags(limit: int = 25, only_active: bool = True) -> AirflowDagsResponse:
    if not is_airflow_configured():
        raise HTTPException(status_code=400, detail="Configura AIRFLOW_API_BASE_URL en .env")

    try:
        dags = list_dags(limit=limit, only_active=only_active)
        return AirflowDagsResponse(total=len(dags), dags=dags)
    except AirflowClientError as error:
        raise HTTPException(status_code=error.status_code, detail=error.detail) from error


@router.post("/airflow/dags/{dag_id}/runs", response_model=AirflowDagRunResponse)
def airflow_trigger_dag_run(dag_id: str, payload: TriggerDagRunRequest) -> AirflowDagRunResponse:
    if not is_airflow_configured():
        raise HTTPException(status_code=400, detail="Configura AIRFLOW_API_BASE_URL en .env")

    try:
        response = trigger_dag_run(
            dag_id=dag_id,
            conf=payload.conf,
            dag_run_id=payload.dag_run_id,
            logical_date=payload.logical_date,
        )
        return AirflowDagRunResponse(**response)
    except AirflowClientError as error:
        raise HTTPException(status_code=error.status_code, detail=error.detail) from error


@router.get("/airflow/dags/{dag_id}/runs/{dag_run_id}", response_model=AirflowDagRunResponse)
def airflow_get_dag_run(dag_id: str, dag_run_id: str) -> AirflowDagRunResponse:
    if not is_airflow_configured():
        raise HTTPException(status_code=400, detail="Configura AIRFLOW_API_BASE_URL en .env")

    try:
        response = get_dag_run(dag_id=dag_id, dag_run_id=dag_run_id)
        return AirflowDagRunResponse(**response)
    except AirflowClientError as error:
        raise HTTPException(status_code=error.status_code, detail=error.detail) from error
