from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.pipeline.service import pipeline_service
from app.schemas import (
    GenerateSyntheticRequest,
    GenerateSyntheticResponse,
    PipelineStatus,
    RunPipelineRequest,
    RunPipelineResponse,
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
