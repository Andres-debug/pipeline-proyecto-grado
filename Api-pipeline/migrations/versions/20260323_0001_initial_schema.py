"""initial schema

Revision ID: 20260323_0001
Revises:
Create Date: 2026-03-23 00:00:00
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa

from app.core.config import settings


revision = "20260323_0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    schema = settings.db_schema

    op.execute(sa.text(f'CREATE SCHEMA IF NOT EXISTS "{schema}"'))

    op.create_table(
        "dim_tiempo",
        sa.Column("id_tiempo", sa.Integer(), nullable=False),
        sa.Column("anio", sa.Integer(), nullable=False),
        sa.Column("semestre", sa.Integer(), nullable=False),
        sa.Column("trimestre", sa.Integer(), nullable=False),
        sa.Column("periodo", sa.String(length=20), nullable=True),
        sa.Column("anio_semestre", sa.String(length=20), nullable=True),
        sa.PrimaryKeyConstraint("id_tiempo"),
        sa.UniqueConstraint("anio", "semestre", name="uq_dim_tiempo_anio_semestre"),
        schema=schema,
    )

    op.create_table(
        "dim_geografia",
        sa.Column("id_pais", sa.Integer(), nullable=False),
        sa.Column("pais_extranjero", sa.String(length=100), nullable=False),
        sa.Column("region", sa.String(length=50), nullable=False),
        sa.PrimaryKeyConstraint("id_pais"),
        sa.UniqueConstraint("pais_extranjero"),
        schema=schema,
    )

    op.create_table(
        "dim_universidad",
        sa.Column("id_universidad", sa.Integer(), nullable=False),
        sa.Column("nombre_universidad", sa.String(length=100), nullable=False),
        sa.Column("tipo", sa.String(length=20), nullable=True),
        sa.Column("ciudad", sa.String(length=50), nullable=False),
        sa.PrimaryKeyConstraint("id_universidad"),
        sa.UniqueConstraint("nombre_universidad"),
        schema=schema,
    )

    op.create_table(
        "dim_tipo_movilidad",
        sa.Column("id_tipo_movilidad", sa.Integer(), nullable=False),
        sa.Column("tipo_mov_est_extranj", sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint("id_tipo_movilidad"),
        sa.UniqueConstraint("tipo_mov_est_extranj"),
        schema=schema,
    )

    op.create_table(
        "kpis_movilidad",
        sa.Column("id_kpi", sa.Integer(), nullable=False),
        sa.Column("kpi", sa.String(length=150), nullable=False),
        sa.Column("valor", sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint("id_kpi"),
        schema=schema,
    )

    op.create_table(
        "fact_movilidad",
        sa.Column("id_hecho", sa.Integer(), nullable=False),
        sa.Column("id_tiempo", sa.Integer(), nullable=False),
        sa.Column("id_pais", sa.Integer(), nullable=False),
        sa.Column("id_universidad", sa.Integer(), nullable=False),
        sa.Column("id_tipo_movilidad", sa.Integer(), nullable=False),
        sa.Column("num_dias_movilidad", sa.Integer(), nullable=True),
        sa.Column("financiacion_total", sa.Numeric(precision=15, scale=2), nullable=True),
        sa.Column("gasto_estimado_directo", sa.Numeric(precision=15, scale=2), nullable=True),
        sa.Column("gasto_estimado_total", sa.Numeric(precision=15, scale=2), nullable=True),
        sa.Column("es_sintetico", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["id_pais"], [f"{schema}.dim_geografia.id_pais"]),
        sa.ForeignKeyConstraint(["id_tiempo"], [f"{schema}.dim_tiempo.id_tiempo"]),
        sa.ForeignKeyConstraint(["id_tipo_movilidad"], [f"{schema}.dim_tipo_movilidad.id_tipo_movilidad"]),
        sa.ForeignKeyConstraint(["id_universidad"], [f"{schema}.dim_universidad.id_universidad"]),
        sa.PrimaryKeyConstraint("id_hecho"),
        schema=schema,
    )

    op.create_index("idx_fact_tiempo", "fact_movilidad", ["id_tiempo"], unique=False, schema=schema)
    op.create_index("idx_fact_pais", "fact_movilidad", ["id_pais"], unique=False, schema=schema)
    op.create_index("idx_fact_universidad", "fact_movilidad", ["id_universidad"], unique=False, schema=schema)
    op.create_index("idx_fact_tipo_mov", "fact_movilidad", ["id_tipo_movilidad"], unique=False, schema=schema)


def downgrade() -> None:
    schema = settings.db_schema

    op.drop_index("idx_fact_tipo_mov", table_name="fact_movilidad", schema=schema)
    op.drop_index("idx_fact_universidad", table_name="fact_movilidad", schema=schema)
    op.drop_index("idx_fact_pais", table_name="fact_movilidad", schema=schema)
    op.drop_index("idx_fact_tiempo", table_name="fact_movilidad", schema=schema)
    op.drop_table("fact_movilidad", schema=schema)
    op.drop_table("kpis_movilidad", schema=schema)
    op.drop_table("dim_tipo_movilidad", schema=schema)
    op.drop_table("dim_universidad", schema=schema)
    op.drop_table("dim_geografia", schema=schema)
    op.drop_table("dim_tiempo", schema=schema)
