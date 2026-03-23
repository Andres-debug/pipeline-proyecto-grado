from __future__ import annotations

from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd


PAISES = [
    "México",
    "España",
    "Brasil",
    "Italia",
    "Grecia",
    "Estados Unidos",
    "Argentina",
    "Chile",
    "Perú",
    "Ecuador",
]

PESO_PAISES = np.array([0.23, 0.2, 0.12, 0.08, 0.05, 0.09, 0.08, 0.06, 0.05, 0.04])

TIPOS_MOVILIDAD = ["Curso corto", "Intercambio", "Pasantía", "Investigación"]
PESO_TIPO = np.array([0.45, 0.25, 0.2, 0.1])

INSTITUCIONES_EXTRANJERAS = [
    "Universidad Autónoma",
    "Instituto Tecnológico Internacional",
    "Universidad Metropolitana",
    "Centro de Investigación Global",
    "Escuela Superior de Innovación",
]


def _sample_days(tipo: str, size: int, rng: np.random.Generator) -> np.ndarray:
    if tipo == "Curso corto":
        return rng.integers(4, 16, size=size)
    if tipo == "Intercambio":
        return rng.integers(90, 181, size=size)
    if tipo == "Pasantía":
        return rng.integers(30, 121, size=size)
    return rng.integers(45, 151, size=size)


def _categorize_duration(days: float | int) -> str:
    if days <= 7:
        return "Corta (≤7 días)"
    if days <= 30:
        return "Media (8-30 días)"
    if days <= 90:
        return "Larga (31-90 días)"
    return "Muy larga (>90 días)"


def generate_synthetic_mobility_data(
    rows: int,
    university: str,
    year_start: int,
    year_end: int,
    seed: int,
) -> pd.DataFrame:
    rng = np.random.default_rng(seed)

    years = rng.integers(year_start, year_end + 1, size=rows)
    semesters = rng.choice([1, 2], size=rows, p=[0.5, 0.5])
    countries = rng.choice(PAISES, size=rows, p=PESO_PAISES)
    mobility_types = rng.choice(TIPOS_MOVILIDAD, size=rows, p=PESO_TIPO)

    days = np.array([
        int(_sample_days(mobility_type, 1, rng)[0]) for mobility_type in mobility_types
    ])

    base_daily_cost = rng.normal(loc=135000, scale=22000, size=rows).clip(70000, 240000)
    mobility_multiplier = np.array([
        0.95 if t == "Curso corto" else 1.2 if t == "Intercambio" else 1.1 if t == "Pasantía" else 1.3
        for t in mobility_types
    ])
    total_funding = (days * base_daily_cost * mobility_multiplier).round(0)

    institution_foreign = rng.choice(INSTITUCIONES_EXTRANJERAS, size=rows)

    df = pd.DataFrame(
        {
            "AÑO": years,
            "SEMESTRE": semesters,
            "UNIVERSIDAD": university,
            "PAIS_EXTRANJERO": countries,
            "INSTITUCION_EXTRANJERA": institution_foreign,
            "TIPO_MOV_EST_EXTRANJ": mobility_types,
            "NUM_DIAS_MOVILIDAD": days,
            "CATEGORIA_DURACION": [
                _categorize_duration(day) for day in days
            ],
            "FINANCIACION_TOTAL": total_funding,
        }
    )

    return df


def save_synthetic_data(
    output_dir: Path,
    rows: int = 2000,
    university: str = "Tecnológico de Antioquia",
    year_start: int = 2022,
    year_end: int = 2026,
    seed: int = 42,
    file_stem: str | None = None,
) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)

    generated_df = generate_synthetic_mobility_data(
        rows=rows,
        university=university,
        year_start=year_start,
        year_end=year_end,
        seed=seed,
    )

    if not file_stem:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_stem = f"movilidades_sintetico_api_{timestamp}"

    output_path = output_dir / f"{file_stem}.csv"
    generated_df.to_csv(output_path, index=False, encoding="utf-8")
    return output_path
