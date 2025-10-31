
-- ============================================================================
-- SCRIPT DE CREACIÓN DE BASE DE DATOS - TURISMO ACADÉMICO MEDELLÍN
-- Proyecto: Arquitectura de BI y Big Data
-- Autor: Proyecto de Grado - Especialización
-- Fecha: 2025-10-31
-- ============================================================================

-- Crear base de datos
CREATE DATABASE turismo_academico_medellin;
\c turismo_academico_medellin;

-- ============================================================================
-- TABLAS DIMENSIONALES
-- ============================================================================

-- Dimensión Tiempo
CREATE TABLE dim_tiempo (
    id_tiempo SERIAL PRIMARY KEY,
    anio INTEGER NOT NULL,
    semestre INTEGER NOT NULL CHECK (semestre IN (1, 2)),
    trimestre INTEGER NOT NULL CHECK (trimestre IN (1, 2)),
    periodo VARCHAR(20),
    anio_semestre VARCHAR(20),
    UNIQUE(anio, semestre)
);

-- Dimensión Geografía
CREATE TABLE dim_geografia (
    id_pais SERIAL PRIMARY KEY,
    pais_extranjero VARCHAR(100) NOT NULL UNIQUE,
    region VARCHAR(50) NOT NULL
);

-- Dimensión Universidad
CREATE TABLE dim_universidad (
    id_universidad SERIAL PRIMARY KEY,
    nombre_universidad VARCHAR(100) NOT NULL UNIQUE,
    tipo VARCHAR(20) CHECK (tipo IN ('Pública', 'Privada')),
    ciudad VARCHAR(50) NOT NULL
);

-- Dimensión Tipo de Movilidad
CREATE TABLE dim_tipo_movilidad (
    id_tipo_movilidad SERIAL PRIMARY KEY,
    tipo_mov_est_extranj VARCHAR(100) NOT NULL UNIQUE
);

-- ============================================================================
-- TABLA DE HECHOS
-- ============================================================================

CREATE TABLE fact_movilidad (
    id_hecho SERIAL PRIMARY KEY,
    id_tiempo INTEGER REFERENCES dim_tiempo(id_tiempo),
    id_pais INTEGER REFERENCES dim_geografia(id_pais),
    id_universidad INTEGER REFERENCES dim_universidad(id_universidad),
    id_tipo_movilidad INTEGER REFERENCES dim_tipo_movilidad(id_tipo_movilidad),
    num_dias_movilidad INTEGER,
    financiacion_total NUMERIC(15, 2),
    gasto_estimado_directo NUMERIC(15, 2),
    gasto_estimado_total NUMERIC(15, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================================
-- ÍNDICES PARA OPTIMIZACIÓN
-- ============================================================================

CREATE INDEX idx_fact_tiempo ON fact_movilidad(id_tiempo);
CREATE INDEX idx_fact_pais ON fact_movilidad(id_pais);
CREATE INDEX idx_fact_universidad ON fact_movilidad(id_universidad);
CREATE INDEX idx_fact_tipo_mov ON fact_movilidad(id_tipo_movilidad);

-- ============================================================================
-- VISTAS PARA POWER BI
-- ============================================================================

-- Vista consolidada para análisis
CREATE VIEW vw_movilidad_completa AS
SELECT 
    f.id_hecho,
    t.anio,
    t.semestre,
    t.anio_semestre,
    g.pais_extranjero,
    g.region,
    u.nombre_universidad,
    u.tipo AS tipo_universidad,
    tm.tipo_mov_est_extranj,
    f.num_dias_movilidad,
    f.financiacion_total,
    f.gasto_estimado_directo,
    f.gasto_estimado_total
FROM fact_movilidad f
JOIN dim_tiempo t ON f.id_tiempo = t.id_tiempo
JOIN dim_geografia g ON f.id_pais = g.id_pais
JOIN dim_universidad u ON f.id_universidad = u.id_universidad
JOIN dim_tipo_movilidad tm ON f.id_tipo_movilidad = tm.id_tipo_movilidad;

-- Vista de KPIs
CREATE VIEW vw_kpis_resumen AS
SELECT 
    COUNT(*) AS total_estudiantes,
    COUNT(DISTINCT f.id_pais) AS paises_representados,
    AVG(f.num_dias_movilidad) AS duracion_promedio_dias,
    SUM(f.gasto_estimado_total) AS impacto_economico_total,
    SUM(f.financiacion_total) AS financiacion_total
FROM fact_movilidad f;

-- ============================================================================
-- COMENTARIOS EN LAS TABLAS
-- ============================================================================

COMMENT ON TABLE fact_movilidad IS 'Tabla de hechos con registros de movilidad estudiantil internacional';
COMMENT ON TABLE dim_tiempo IS 'Dimensión temporal con años y semestres';
COMMENT ON TABLE dim_geografia IS 'Dimensión geográfica con países y regiones';
COMMENT ON TABLE dim_universidad IS 'Dimensión de universidades de Medellín';
COMMENT ON TABLE dim_tipo_movilidad IS 'Dimensión de tipos de movilidad académica';

-- ============================================================================
-- FIN DEL SCRIPT
-- ============================================================================

-- Para cargar datos desde CSV usar:
-- \copy dim_tiempo FROM 'dim_tiempo.csv' DELIMITER ',' CSV HEADER;
-- \copy dim_geografia FROM 'dim_geografia.csv' DELIMITER ',' CSV HEADER;
-- \copy dim_universidad FROM 'dim_universidad.csv' DELIMITER ',' CSV HEADER;
-- \copy dim_tipo_movilidad FROM 'dim_tipo_movilidad.csv' DELIMITER ',' CSV HEADER;
-- \copy fact_movilidad FROM 'fact_movilidad.csv' DELIMITER ',' CSV HEADER;
