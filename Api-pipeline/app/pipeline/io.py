from __future__ import annotations

import json
import unicodedata
from pathlib import Path
from typing import Any

import pandas as pd


def normalize_column_name(name: str) -> str:
    text = str(name)
    text = "".join(
        char
        for char in unicodedata.normalize("NFD", text)
        if unicodedata.category(char) != "Mn"
    )
    return text.strip().upper().replace(" ", "_")


def _detect_header_row(df_raw: pd.DataFrame, max_scan_rows: int = 25) -> int | None:
    scan_limit = min(max_scan_rows, len(df_raw))
    for index in range(scan_limit):
        row_values = [normalize_column_name(value) for value in df_raw.iloc[index].tolist() if pd.notna(value)]
        row_set = set(row_values)
        has_year = "AÑO" in row_set or "ANO" in row_set
        has_semester = "SEMESTRE" in row_set
        if has_year and has_semester:
            return index
    return None


def _read_excel_all_sheets(path: Path) -> pd.DataFrame:
    excel_file = pd.ExcelFile(path)
    parsed_frames: list[pd.DataFrame] = []

    for sheet_name in excel_file.sheet_names:
        sheet_raw = pd.read_excel(path, sheet_name=sheet_name, header=None)
        header_row_index = _detect_header_row(sheet_raw)

        if header_row_index is None:
            continue

        header_values = sheet_raw.iloc[header_row_index].tolist()
        sheet_data = sheet_raw.iloc[header_row_index + 1 :].copy()
        sheet_data.columns = header_values
        sheet_data = sheet_data.dropna(how="all")

        if sheet_data.empty:
            continue

        sheet_data["__SHEET_NAME"] = sheet_name
        parsed_frames.append(sheet_data)

    if not parsed_frames:
        return pd.DataFrame()

    return pd.concat(parsed_frames, ignore_index=True)


def read_flexible_file(path: Path) -> pd.DataFrame:
    suffix = path.suffix.lower()
    if suffix in {".xlsx", ".xls"}:
        return _read_excel_all_sheets(path)
    if suffix == ".csv":
        return pd.read_csv(path, na_values=["#N/A", "N/A", "NA", "", " "], keep_default_na=True)
    if suffix == ".json":
        try:
            return pd.read_json(path)
        except ValueError:
            return pd.read_json(path, lines=True)
    raise ValueError(f"Formato no soportado: {suffix}")


def load_mapping(mapping_path: Path) -> dict[str, Any]:
    with mapping_path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _match_column(df_columns_normalized: set[str], candidates: list[str]) -> str | None:
    for candidate in candidates:
        candidate_norm = normalize_column_name(candidate)
        if candidate_norm in df_columns_normalized:
            return candidate_norm
    return None


def map_columns(
    source_df: pd.DataFrame,
    source_key: str,
    canonical_columns: list[str],
    source_map: dict[str, Any],
) -> pd.DataFrame:
    df = source_df.copy()
    df.columns = [normalize_column_name(col) for col in df.columns]

    mapping = source_map.get(source_key, {})
    renames: dict[str, str] = {}

    for canonical in canonical_columns:
        candidates = mapping.get(canonical, [canonical])
        matched = _match_column(set(df.columns), candidates)
        if matched is not None:
            renames[matched] = canonical

    if renames:
        df = df.rename(columns=renames)

    for column in canonical_columns:
        if column not in df.columns:
            df[column] = pd.NA

    for column in ["AÑO", "SEMESTRE"]:
        if column in df.columns:
            df[column] = pd.to_numeric(df[column], errors="coerce").astype("Int64")

    for column in ["NUM_DIAS_MOVILIDAD", "FINANCIACION_TOTAL"]:
        if column in df.columns:
            df[column] = pd.to_numeric(df[column], errors="coerce")

    if "FINANCIACION_TOTAL" in df.columns and df["FINANCIACION_TOTAL"].isna().all():
        partial_columns = []
        for candidate in [
            "VALOR_FINANCIACION_NACIONAL",
            "VALOR_FINANCIACION_INTERNAC",
            "VALOR_FINANCIACION_INTERNACIONAL",
            "FINANCIACION_NACIONAL",
            "FINANCIACION_INTERNACIONAL",
        ]:
            normalized = normalize_column_name(candidate)
            if normalized in df.columns:
                df[normalized] = pd.to_numeric(df[normalized], errors="coerce")
                partial_columns.append(normalized)
        if partial_columns:
            df["FINANCIACION_TOTAL"] = sum(df[col] for col in partial_columns)

    if "CATEGORIA_DURACION" in df.columns and df["CATEGORIA_DURACION"].isna().all():
        if "NUM_DIAS_MOVILIDAD" in df.columns:
            def _duration_category(value: Any) -> str | None:
                try:
                    value_float = float(value)
                except Exception:
                    return pd.NA
                if pd.isna(value_float):
                    return pd.NA
                if value_float <= 30:
                    return "CORTA"
                if value_float <= 90:
                    return "MEDIA"
                return "LARGA"

            df["CATEGORIA_DURACION"] = df["NUM_DIAS_MOVILIDAD"].apply(_duration_category)

    for column in [
        "UNIVERSIDAD",
        "PAIS_EXTRANJERO",
        "INSTITUCION_EXTRANJERA",
        "TIPO_MOV_EST_EXTRANJ",
        "CATEGORIA_DURACION",
    ]:
        if column in df.columns:
            df[column] = df[column].astype("string")

    return df[canonical_columns].copy()
