from __future__ import annotations

from dataclasses import dataclass


@dataclass
class DatabaseConfig:
    db_url: str | None


def is_database_configured(db_url: str | None) -> bool:
    return bool(db_url and db_url.strip())
