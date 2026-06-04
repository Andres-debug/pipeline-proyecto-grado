from __future__ import annotations

from typing import Any

import pandas as pd


UNIVERSITY_DEFAULTS: dict[str, dict[str, str]] = {
    "IUSH": {"TIPO": "Privada", "CIUDAD": "Medellín"},
    "UNIVERSIDAD DE ANTIOQUIA": {"TIPO": "Pública", "CIUDAD": "Medellín"},
    "UNAC": {"TIPO": "Privada", "CIUDAD": "Medellín"},
    "TECNOLÓGICO DE ANTIOQUIA": {"TIPO": "Pública", "CIUDAD": "Medellín"},
    "TECNOLOGICO DE ANTIOQUIA": {"TIPO": "Pública", "CIUDAD": "Medellín"},
}


def classify_region(country: Any) -> str:
    country_upper = str(country).upper()
    if any(item in country_upper for item in ["MÉXICO", "ESTADOS UNIDOS", "BRASIL", "VENEZUELA"]):
        return "América"
    if any(item in country_upper for item in ["ESPAÑA", "ITALIA", "GRECIA", "RUMANIA", "TURQUÍA"]):
        return "Europa"
    return "Otro"


def build_dim_tiempo(df: pd.DataFrame) -> pd.DataFrame:
    dim_tiempo = df[["AÑO", "SEMESTRE", "PERIODO"]].copy()
    dim_tiempo = dim_tiempo.dropna(subset=["AÑO", "SEMESTRE"])
    dim_tiempo = dim_tiempo.drop_duplicates().reset_index(drop=True)
    dim_tiempo["ID_TIEMPO"] = range(1, len(dim_tiempo) + 1)
    dim_tiempo["TRIMESTRE"] = dim_tiempo["SEMESTRE"].apply(lambda value: 1 if value == 1 else 2)
    dim_tiempo["ANIO_SEMESTRE"] = dim_tiempo["AÑO"].astype(str) + "-S" + dim_tiempo["SEMESTRE"].astype(str)
    return dim_tiempo[["ID_TIEMPO", "AÑO", "SEMESTRE", "TRIMESTRE", "PERIODO", "ANIO_SEMESTRE"]].copy()


def build_dim_geografia(df: pd.DataFrame) -> pd.DataFrame:
    dim_geografia = df[["PAIS_EXTRANJERO"]].copy()
    dim_geografia = dim_geografia.dropna(subset=["PAIS_EXTRANJERO"])
    dim_geografia = dim_geografia[dim_geografia["PAIS_EXTRANJERO"].astype("string").str.strip() != ""]
    dim_geografia = dim_geografia.drop_duplicates().reset_index(drop=True)
    dim_geografia["ID_PAIS"] = range(1, len(dim_geografia) + 1)
    dim_geografia["REGION"] = dim_geografia["PAIS_EXTRANJERO"].apply(classify_region)
    return dim_geografia[["ID_PAIS", "PAIS_EXTRANJERO", "REGION"]].copy()


def build_dim_universidad(df: pd.DataFrame) -> pd.DataFrame:
    unique_universities = (
        df[["UNIVERSIDAD"]]
        .dropna()
        .drop_duplicates()
        .sort_values("UNIVERSIDAD")
        .reset_index(drop=True)
    )
    unique_universities["ID_UNIVERSIDAD"] = range(1, len(unique_universities) + 1)

    normalized_names = unique_universities["UNIVERSIDAD"].astype(str).str.upper()
    unique_universities["TIPO"] = normalized_names.map(
        lambda value: UNIVERSITY_DEFAULTS.get(value, {}).get("TIPO", "No definida")
    )
    unique_universities["CIUDAD"] = normalized_names.map(
        lambda value: UNIVERSITY_DEFAULTS.get(value, {}).get("CIUDAD", "Medellín")
    )

    unique_universities = unique_universities.rename(columns={"UNIVERSIDAD": "NOMBRE_UNIVERSIDAD"})
    return unique_universities[["ID_UNIVERSIDAD", "NOMBRE_UNIVERSIDAD", "TIPO", "CIUDAD"]].copy()


def build_dim_tipo_movilidad(df: pd.DataFrame) -> pd.DataFrame:
    dim_tipo = df[["TIPO_MOV_EST_EXTRANJ"]].copy()
    dim_tipo = dim_tipo.dropna(subset=["TIPO_MOV_EST_EXTRANJ"])
    dim_tipo = dim_tipo[dim_tipo["TIPO_MOV_EST_EXTRANJ"].astype("string").str.strip() != ""]
    dim_tipo = dim_tipo.drop_duplicates().reset_index(drop=True)
    dim_tipo["ID_TIPO_MOVILIDAD"] = range(1, len(dim_tipo) + 1)
    return dim_tipo[["ID_TIPO_MOVILIDAD", "TIPO_MOV_EST_EXTRANJ"]].copy()


def build_fact_movilidad(
    df: pd.DataFrame,
    dim_tiempo: pd.DataFrame,
    dim_geografia: pd.DataFrame,
    dim_universidad: pd.DataFrame,
    dim_tipo_movilidad: pd.DataFrame,
) -> pd.DataFrame:
    fact = df.copy()

    fact = fact.merge(dim_tiempo[["ID_TIEMPO", "AÑO", "SEMESTRE"]], on=["AÑO", "SEMESTRE"], how="left")
    fact = fact.merge(dim_geografia[["ID_PAIS", "PAIS_EXTRANJERO"]], on="PAIS_EXTRANJERO", how="left")
    fact = fact.merge(
        dim_universidad[["ID_UNIVERSIDAD", "NOMBRE_UNIVERSIDAD"]],
        left_on="UNIVERSIDAD",
        right_on="NOMBRE_UNIVERSIDAD",
        how="left",
    )
    fact = fact.merge(
        dim_tipo_movilidad[["ID_TIPO_MOVILIDAD", "TIPO_MOV_EST_EXTRANJ"]],
        on="TIPO_MOV_EST_EXTRANJ",
        how="left",
    )

    fact_final = fact[
        [
            "ID_TIEMPO",
            "ID_PAIS",
            "ID_UNIVERSIDAD",
            "ID_TIPO_MOVILIDAD",
            "NUM_DIAS_MOVILIDAD",
            "FINANCIACION_TOTAL",
            "GASTO_ESTIMADO_DIRECTO",
            "GASTO_ESTIMADO_TOTAL",
            "ES_SINTETICO",
        ]
    ].copy()

    fact_final["ID_HECHO"] = range(1, len(fact_final) + 1)

    # Evita violaciones NOT NULL/FK al cargar en PostgreSQL.
    fact_final = fact_final.dropna(
        subset=["ID_TIEMPO", "ID_PAIS", "ID_UNIVERSIDAD", "ID_TIPO_MOVILIDAD", "ES_SINTETICO"]
    ).copy()

    for key_col in ["ID_TIEMPO", "ID_PAIS", "ID_UNIVERSIDAD", "ID_TIPO_MOVILIDAD", "ES_SINTETICO"]:
        fact_final[key_col] = fact_final[key_col].astype(int)

    fact_final["ID_HECHO"] = range(1, len(fact_final) + 1)

    return fact_final[
        [
            "ID_HECHO",
            "ID_TIEMPO",
            "ID_PAIS",
            "ID_UNIVERSIDAD",
            "ID_TIPO_MOVILIDAD",
            "NUM_DIAS_MOVILIDAD",
            "FINANCIACION_TOTAL",
            "GASTO_ESTIMADO_DIRECTO",
            "GASTO_ESTIMADO_TOTAL",
            "ES_SINTETICO",
        ]
    ].copy()


def build_kpis(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame(columns=["KPI", "Valor"])

    last_year = df["AÑO"].max()
    last_year_df = df[df["AÑO"] == last_year]

    kpis: dict[str, Any] = {
        "Total_Estudiantes_Internacionales": len(df),
        "Paises_Representados": df["PAIS_EXTRANJERO"].nunique(),
        "Duracion_Promedio_Dias": float(df["NUM_DIAS_MOVILIDAD"].mean()),
        "Duracion_Mediana_Dias": float(df["NUM_DIAS_MOVILIDAD"].median()),
        "Impacto_Economico_Total_COP": float(df["GASTO_ESTIMADO_TOTAL"].sum()),
        "Impacto_Economico_Total_USD": float(df["GASTO_ESTIMADO_TOTAL"].sum() / 4000),
        "Financiacion_Total_COP": float(df["FINANCIACION_TOTAL"].sum()),
        "Estudiantes_Por_Universidad_Promedio": float(len(df) / max(df["UNIVERSIDAD"].nunique(), 1)),
        "Instituciones_Extranjeras": df["INSTITUCION_EXTRANJERA"].nunique(),
        "Pais_Principal": df["PAIS_EXTRANJERO"].value_counts().index[0] if not df["PAIS_EXTRANJERO"].dropna().empty else "N/A",
        "Tipo_Movilidad_Principal": df["TIPO_MOV_EST_EXTRANJ"].value_counts().index[0] if not df["TIPO_MOV_EST_EXTRANJ"].dropna().empty else "N/A",
        f"Estudiantes_{last_year}": len(last_year_df),
        f"Impacto_Economico_{last_year}_COP": float(last_year_df["GASTO_ESTIMADO_TOTAL"].sum()),
        "Tasa_Crecimiento_Anual_Pct": 0.0,
    }

    return pd.DataFrame(list(kpis.items()), columns=["KPI", "VALOR"])
