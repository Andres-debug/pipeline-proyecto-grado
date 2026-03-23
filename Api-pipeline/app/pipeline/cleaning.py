from __future__ import annotations

import pandas as pd


COUNTRY_MAPPING = {
    "ESTADOS UNIDOS DE AMÉRICA": "Estados Unidos",
    "ESTADOS UNIDOS": "Estados Unidos",
    "USA": "Estados Unidos",
    "US": "Estados Unidos",
    "MÉXICO": "México",
    "MEXICO": "México",
    "ESPAÑA": "España",
    "BRASIL": "Brasil",
    "ITALY": "Italia",
    "ITALIA": "Italia",
    "GRECIA": "Grecia",
    "GREECE": "Grecia",
    "TURQUÍA": "Turquía",
    "TURKEY": "Turquía",
    "RUMANÍA": "Rumania",
    "ROMANIA": "Rumania",
    "VENEZUELA": "Venezuela",
}

UNIVERSITY_MAPPING = {
    "TECNOLOGICO DE ANTIOQUIA": "Tecnológico de Antioquia",
    "TECNOLÓGICO DE ANTIOQUIA": "Tecnológico de Antioquia",
    "TDEA": "Tecnológico de Antioquia",
}

NA_TOKENS = {
    "#N/A",
    "N/A",
    "NA",
    "NAN",
    "NULL",
    "NONE",
    "",
    "-",
}


def normalize_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    cleaned = df.copy()

    object_columns = cleaned.select_dtypes(include=["object", "string"]).columns
    for column in object_columns:
        series = cleaned[column].astype("string").str.strip()
        upper_series = series.str.upper()
        cleaned[column] = series.mask(upper_series.isin(NA_TOKENS), pd.NA)

    return cleaned


def strip_text_columns(df: pd.DataFrame) -> pd.DataFrame:
    cleaned = df.copy()
    text_columns = cleaned.select_dtypes(include=["object", "string"]).columns
    for column in text_columns:
        cleaned[column] = cleaned[column].astype("string").str.strip()
    return cleaned


def drop_empty_rows(df: pd.DataFrame) -> pd.DataFrame:
    return df.dropna(how="all").copy()


def standardize_countries(df: pd.DataFrame, column: str = "PAIS_EXTRANJERO") -> pd.DataFrame:
    cleaned = df.copy()
    if column in cleaned.columns:
        cleaned[column] = (
            cleaned[column]
            .astype("string")
            .str.upper()
            .str.strip()
            .replace(COUNTRY_MAPPING)
        )
    return cleaned


def standardize_universities(df: pd.DataFrame, column: str = "UNIVERSIDAD") -> pd.DataFrame:
    cleaned = df.copy()
    if column in cleaned.columns:
        original = cleaned[column].astype("string").str.strip()
        normalized = original.str.upper().replace(UNIVERSITY_MAPPING)
        cleaned[column] = normalized.where(normalized.notna(), original)
    return cleaned


def convert_common_types(df: pd.DataFrame) -> pd.DataFrame:
    cleaned = df.copy()

    numeric_columns = [
        "AÑO",
        "SEMESTRE",
        "NUM_DIAS_MOVILIDAD",
        "FINANCIACION_TOTAL",
    ]
    for column in numeric_columns:
        if column in cleaned.columns:
            cleaned[column] = pd.to_numeric(cleaned[column], errors="coerce")

    for column in ["AÑO", "SEMESTRE"]:
        if column in cleaned.columns:
            cleaned[column] = cleaned[column].astype("Int64")

    return cleaned


def _categorize_duration(days: float | int | None) -> str:
    if pd.isna(days):
        return "No especificado"
    if days <= 7:
        return "Corta (≤7 días)"
    if days <= 30:
        return "Media (8-30 días)"
    if days <= 90:
        return "Larga (31-90 días)"
    return "Muy larga (>90 días)"


def derive_columns(df: pd.DataFrame) -> pd.DataFrame:
    enriched = df.copy()

    if {"AÑO", "SEMESTRE"}.issubset(enriched.columns):
        enriched["PERIODO"] = enriched["AÑO"].astype("string") + "-" + enriched["SEMESTRE"].astype("string")

    if "NUM_DIAS_MOVILIDAD" in enriched.columns and "CATEGORIA_DURACION" in enriched.columns:
        missing_category = enriched["CATEGORIA_DURACION"].isna() | (enriched["CATEGORIA_DURACION"].astype("string").str.strip() == "")
        enriched.loc[missing_category, "CATEGORIA_DURACION"] = enriched.loc[missing_category, "NUM_DIAS_MOVILIDAD"].apply(_categorize_duration)
    elif "NUM_DIAS_MOVILIDAD" in enriched.columns:
        enriched["CATEGORIA_DURACION"] = enriched["NUM_DIAS_MOVILIDAD"].apply(_categorize_duration)

    if "FINANCIACION_TOTAL" in enriched.columns:
        enriched["FINANCIACION_TOTAL"] = pd.to_numeric(enriched["FINANCIACION_TOTAL"], errors="coerce").fillna(0)
    else:
        enriched["FINANCIACION_TOTAL"] = 0

    if "GASTO_ESTIMADO_DIRECTO" not in enriched.columns:
        enriched["GASTO_ESTIMADO_DIRECTO"] = pd.to_numeric(
            enriched.get("NUM_DIAS_MOVILIDAD", 0), errors="coerce"
        ).fillna(0) * 100000

    if "GASTO_ESTIMADO_TOTAL" not in enriched.columns:
        enriched["GASTO_ESTIMADO_TOTAL"] = enriched["GASTO_ESTIMADO_DIRECTO"] * 1.5

    if "ES_SINTETICO" in enriched.columns:
        enriched["ES_SINTETICO"] = pd.to_numeric(enriched["ES_SINTETICO"], errors="coerce").fillna(0).astype("Int64")
    else:
        enriched["ES_SINTETICO"] = 0

    return enriched


def clean_dataset(df: pd.DataFrame) -> pd.DataFrame:
    cleaned = normalize_missing_values(df)
    cleaned = drop_empty_rows(cleaned)
    cleaned = strip_text_columns(cleaned)
    cleaned = standardize_countries(cleaned)
    cleaned = standardize_universities(cleaned)
    cleaned = convert_common_types(cleaned)
    cleaned = derive_columns(cleaned)
    return cleaned.drop_duplicates().reset_index(drop=True)
