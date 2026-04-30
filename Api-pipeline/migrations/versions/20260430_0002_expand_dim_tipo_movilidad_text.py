"""expand dim_tipo_movilidad text length

Revision ID: 20260430_0002
Revises: 20260323_0001
Create Date: 2026-04-30 00:00:00
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa

from app.core.config import settings


revision = "20260430_0002"
down_revision = "20260323_0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    schema = settings.db_schema

    op.alter_column(
        "dim_tipo_movilidad",
        "tipo_mov_est_extranj",
        schema=schema,
        existing_type=sa.String(length=100),
        type_=sa.Text(),
        existing_nullable=False,
    )


def downgrade() -> None:
    schema = settings.db_schema

    op.alter_column(
        "dim_tipo_movilidad",
        "tipo_mov_est_extranj",
        schema=schema,
        existing_type=sa.Text(),
        type_=sa.String(length=100),
        existing_nullable=False,
    )
