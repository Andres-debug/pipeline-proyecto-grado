from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class RunPipelineRequest(BaseModel):
    iush_filename: str | None = Field(default=None)
    docentes_filename: str | None = Field(default=None)
    input_files: list[str] | None = Field(default=None)
    auto_discover: bool = Field(default=True)


class PipelineStatus(BaseModel):
    last_run_at: datetime | None = None
    status: str = "idle"
    details: dict[str, Any] = Field(default_factory=dict)


class RunPipelineResponse(BaseModel):
    status: str
    message: str
    rows_consolidated: int
    output_files: dict[str, str]
    dimensions: dict[str, int]
    kpis_total: int
    warnings: list[str] = Field(default_factory=list)


class GenerateSyntheticRequest(BaseModel):
    rows: int = Field(default=2000, ge=100, le=200000)
    university: str = Field(default="Tecnológico de Antioquia")
    year_start: int = Field(default=2022, ge=2015, le=2100)
    year_end: int = Field(default=2026, ge=2015, le=2100)
    seed: int = Field(default=42, ge=0)
    file_stem: str | None = Field(default=None)


class GenerateSyntheticResponse(BaseModel):
    status: str
    message: str
    file_path: str
    rows_generated: int
