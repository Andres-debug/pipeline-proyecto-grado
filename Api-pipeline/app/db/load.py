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

    kpis_db = kpis.copy()
    kpis_db["VALOR"] = kpis_db["VALOR"].astype(str)

    with engine.begin() as connection:
        connection.execute(text(f'TRUNCATE TABLE "{schema}"."fact_movilidad" RESTART IDENTITY CASCADE'))
        connection.execute(text(f'TRUNCATE TABLE "{schema}"."dim_tiempo" RESTART IDENTITY CASCADE'))
        connection.execute(text(f'TRUNCATE TABLE "{schema}"."dim_geografia" RESTART IDENTITY CASCADE'))
        connection.execute(text(f'TRUNCATE TABLE "{schema}"."dim_universidad" RESTART IDENTITY CASCADE'))
        connection.execute(text(f'TRUNCATE TABLE "{schema}"."dim_tipo_movilidad" RESTART IDENTITY CASCADE'))
        connection.execute(text(f'TRUNCATE TABLE "{schema}"."kpis_movilidad" RESTART IDENTITY CASCADE'))

    dim_tiempo.to_sql("dim_tiempo", engine, schema=schema, if_exists="append", index=False)
    dim_geografia.to_sql("dim_geografia", engine, schema=schema, if_exists="append", index=False)
    dim_universidad.to_sql("dim_universidad", engine, schema=schema, if_exists="append", index=False)
    dim_tipo_movilidad.to_sql("dim_tipo_movilidad", engine, schema=schema, if_exists="append", index=False)
    fact_movilidad.to_sql("fact_movilidad", engine, schema=schema, if_exists="append", index=False)
    kpis_db.to_sql("kpis_movilidad", engine, schema=schema, if_exists="append", index=False)

    return {
        "dim_tiempo": f"{schema}.dim_tiempo",
        "dim_geografia": f"{schema}.dim_geografia",
        "dim_universidad": f"{schema}.dim_universidad",
        "dim_tipo_movilidad": f"{schema}.dim_tipo_movilidad",
        "fact_movilidad": f"{schema}.fact_movilidad",
        "kpis_movilidad": f"{schema}.kpis_movilidad",
    }
