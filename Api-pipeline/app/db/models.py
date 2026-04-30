from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, Numeric, String, Text, UniqueConstraint, func
from sqlalchemy.orm import Mapped, declarative_base, mapped_column

from app.core.config import settings


Base = declarative_base()


class DimTiempo(Base):
    __tablename__ = "dim_tiempo"
    __table_args__ = (
        UniqueConstraint("anio", "semestre", name="uq_dim_tiempo_anio_semestre"),
        {"schema": settings.db_schema},
    )

    id_tiempo: Mapped[int] = mapped_column(Integer, primary_key=True)
    anio: Mapped[int] = mapped_column(Integer, nullable=False)
    semestre: Mapped[int] = mapped_column(Integer, nullable=False)
    trimestre: Mapped[int] = mapped_column(Integer, nullable=False)
    periodo: Mapped[str | None] = mapped_column(String(20), nullable=True)
    anio_semestre: Mapped[str | None] = mapped_column(String(20), nullable=True)


class DimGeografia(Base):
    __tablename__ = "dim_geografia"
    __table_args__ = {"schema": settings.db_schema}

    id_pais: Mapped[int] = mapped_column(Integer, primary_key=True)
    pais_extranjero: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    region: Mapped[str] = mapped_column(String(50), nullable=False)


class DimUniversidad(Base):
    __tablename__ = "dim_universidad"
    __table_args__ = {"schema": settings.db_schema}

    id_universidad: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre_universidad: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    tipo: Mapped[str | None] = mapped_column(String(20), nullable=True)
    ciudad: Mapped[str] = mapped_column(String(50), nullable=False)


class DimTipoMovilidad(Base):
    __tablename__ = "dim_tipo_movilidad"
    __table_args__ = {"schema": settings.db_schema}

    id_tipo_movilidad: Mapped[int] = mapped_column(Integer, primary_key=True)
    tipo_mov_est_extranj: Mapped[str] = mapped_column(Text, nullable=False, unique=True)


class FactMovilidad(Base):
    __tablename__ = "fact_movilidad"
    __table_args__ = {"schema": settings.db_schema}

    id_hecho: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_tiempo: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(f"{settings.db_schema}.dim_tiempo.id_tiempo"),
        nullable=False,
    )
    id_pais: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(f"{settings.db_schema}.dim_geografia.id_pais"),
        nullable=False,
    )
    id_universidad: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(f"{settings.db_schema}.dim_universidad.id_universidad"),
        nullable=False,
    )
    id_tipo_movilidad: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(f"{settings.db_schema}.dim_tipo_movilidad.id_tipo_movilidad"),
        nullable=False,
    )
    num_dias_movilidad: Mapped[int | None] = mapped_column(Integer, nullable=True)
    financiacion_total: Mapped[float | None] = mapped_column(Numeric(15, 2), nullable=True)
    gasto_estimado_directo: Mapped[float | None] = mapped_column(Numeric(15, 2), nullable=True)
    gasto_estimado_total: Mapped[float | None] = mapped_column(Numeric(15, 2), nullable=True)
    es_sintetico: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())


class KpiMovilidad(Base):
    __tablename__ = "kpis_movilidad"
    __table_args__ = {"schema": settings.db_schema}

    id_kpi: Mapped[int] = mapped_column(Integer, primary_key=True)
    kpi: Mapped[str] = mapped_column(String(150), nullable=False)
    valor: Mapped[str] = mapped_column(Text, nullable=False)
