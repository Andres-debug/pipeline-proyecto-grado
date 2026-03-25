from __future__ import annotations

import pandas as pd
from sqlalchemy import text

from app.core.config import settings
from app.db.connection import get_engine


def load_star_to_postgres(
    dim_tiempo: pd.DataFrame,
    dim_geografia: pd.DataFrame,
    dim_universidad: pd.DataFrame,
    dim_tipo_movilidad: pd.DataFrame,
    fact_movilidad: pd.DataFrame,
    kpis: pd.DataFrame,
) -> dict[str, str]:
    schema = settings.db_schema
    engine = get_engine()

    dim_tiempo_db = dim_tiempo.rename(
        columns={
            "ID_TIEMPO": "id_tiempo",
            "AÑO": "anio",
            "SEMESTRE": "semestre",
            "TRIMESTRE": "trimestre",
            "PERIODO": "periodo",
            "ANIO_SEMESTRE": "anio_semestre",
        }
    )
    dim_geografia_db = dim_geografia.rename(
        columns={
            "ID_PAIS": "id_pais",
            "PAIS_EXTRANJERO": "pais_extranjero",
            "REGION": "region",
        }
    )
    dim_universidad_db = dim_universidad.rename(
        columns={
            "ID_UNIVERSIDAD": "id_universidad",
            "NOMBRE_UNIVERSIDAD": "nombre_universidad",
            "TIPO": "tipo",
            "CIUDAD": "ciudad",
        }
    )
    dim_tipo_movilidad_db = dim_tipo_movilidad.rename(
        columns={
            "ID_TIPO_MOVILIDAD": "id_tipo_movilidad",
            "TIPO_MOV_EST_EXTRANJ": "tipo_mov_est_extranj",
        }
    )
    fact_movilidad_db = fact_movilidad.rename(
        columns={
            "ID_HECHO": "id_hecho",
            "ID_TIEMPO": "id_tiempo",
            "ID_PAIS": "id_pais",
            "ID_UNIVERSIDAD": "id_universidad",
            "ID_TIPO_MOVILIDAD": "id_tipo_movilidad",
            "NUM_DIAS_MOVILIDAD": "num_dias_movilidad",
            "FINANCIACION_TOTAL": "financiacion_total",
            "GASTO_ESTIMADO_DIRECTO": "gasto_estimado_directo",
            "GASTO_ESTIMADO_TOTAL": "gasto_estimado_total",
            "ES_SINTETICO": "es_sintetico",
        }
    )
    kpis_db = kpis.rename(columns={"KPI": "kpi", "Valor": "valor"}).copy()
    kpis_db["valor"] = kpis_db["valor"].astype(str)

    with engine.begin() as connection:
        connection.execute(text(f'TRUNCATE TABLE "{schema}"."fact_movilidad" RESTART IDENTITY CASCADE'))
        connection.execute(text(f'TRUNCATE TABLE "{schema}"."dim_tiempo" RESTART IDENTITY CASCADE'))
        connection.execute(text(f'TRUNCATE TABLE "{schema}"."dim_geografia" RESTART IDENTITY CASCADE'))
        connection.execute(text(f'TRUNCATE TABLE "{schema}"."dim_universidad" RESTART IDENTITY CASCADE'))
        connection.execute(text(f'TRUNCATE TABLE "{schema}"."dim_tipo_movilidad" RESTART IDENTITY CASCADE'))
        connection.execute(text(f'TRUNCATE TABLE "{schema}"."kpis_movilidad" RESTART IDENTITY CASCADE'))

    dim_tiempo_db.to_sql("dim_tiempo", engine, schema=schema, if_exists="append", index=False)
    dim_geografia_db.to_sql("dim_geografia", engine, schema=schema, if_exists="append", index=False)
    dim_universidad_db.to_sql("dim_universidad", engine, schema=schema, if_exists="append", index=False)
    dim_tipo_movilidad_db.to_sql("dim_tipo_movilidad", engine, schema=schema, if_exists="append", index=False)
    fact_movilidad_db.to_sql("fact_movilidad", engine, schema=schema, if_exists="append", index=False)
    kpis_db.to_sql("kpis_movilidad", engine, schema=schema, if_exists="append", index=False)

    return {
        "dim_tiempo": f"{schema}.dim_tiempo",
        "dim_geografia": f"{schema}.dim_geografia",
        "dim_universidad": f"{schema}.dim_universidad",
        "dim_tipo_movilidad": f"{schema}.dim_tipo_movilidad",
        "fact_movilidad": f"{schema}.fact_movilidad",
        "kpis_movilidad": f"{schema}.kpis_movilidad",
    }
