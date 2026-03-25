from __future__ import annotations

import logging

import psycopg
from psycopg import sql
from sqlalchemy import text
from sqlalchemy.engine.url import make_url

from app.core.config import settings
from app.db.connection import get_engine
from app.db.models import Base


logger = logging.getLogger(__name__)


def ensure_database_exists() -> bool:
    if not settings.db_url:
        logger.info("DB_URL no configurado, se omite creación de base de datos.")
        return False

    db_url = make_url(settings.db_url)
    if not db_url.database:
        raise ValueError("DB_URL debe incluir el nombre de la base de datos")

    target_database = db_url.database
    admin_database = "postgres"

    with psycopg.connect(
        dbname=admin_database,
        user=db_url.username,
        password=db_url.password,
        host=db_url.host,
        port=db_url.port,
        autocommit=True,
    ) as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (target_database,))
            exists = cursor.fetchone() is not None
            if exists:
                logger.info("Base de datos '%s' ya existe.", target_database)
                return False

            cursor.execute(sql.SQL("CREATE DATABASE {}") .format(sql.Identifier(target_database)))
            logger.info("Base de datos '%s' creada.", target_database)
            return True


def create_schema_and_tables() -> None:
    if not settings.db_url:
        logger.info("DB_URL no configurado, se omite creación de esquema/tablas.")
        return

    engine = get_engine()
    with engine.begin() as connection:
        connection.execute(text(f'CREATE SCHEMA IF NOT EXISTS "{settings.db_schema}"'))

    Base.metadata.create_all(bind=engine, checkfirst=True)
    logger.info("Esquema y tablas ORM verificados en PostgreSQL.")


def initialize_database() -> None:
    ensure_database_exists()
    create_schema_and_tables()
