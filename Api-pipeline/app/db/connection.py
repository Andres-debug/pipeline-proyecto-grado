from __future__ import annotations

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

from app.core.config import settings


def get_engine() -> Engine:
    if not settings.db_url:
        raise ValueError("DB_URL no está configurado en el entorno")
    return create_engine(
        settings.db_url,
        pool_pre_ping=True,
        pool_size=2,
        max_overflow=1,
        pool_timeout=30,
    )


def test_connection() -> None:
    engine = get_engine()
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
