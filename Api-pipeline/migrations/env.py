from __future__ import annotations

from logging.config import fileConfig
from pathlib import Path
import sys

from alembic import context
from sqlalchemy import engine_from_config, pool


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.core.config import settings
from app.db.bootstrap import ensure_database_exists
from app.db.models import Base


config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

config.set_main_option("sqlalchemy.url", settings.db_url or "")

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    if not url:
        raise ValueError("DB_URL no está configurado. Configura .env antes de ejecutar Alembic.")

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    ensure_database_exists()

    section = config.get_section(config.config_ini_section) or {}
    connectable = engine_from_config(
        section,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata, compare_type=True)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
