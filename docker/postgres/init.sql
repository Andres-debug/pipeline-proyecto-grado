-- Script ejecutado una sola vez al inicializar el contenedor de PostgreSQL.
-- Crea las bases de datos para la API y para Airflow si no existen.

SELECT 'CREATE DATABASE turismo_academico_medellin'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'turismo_academico_medellin')\gexec

SELECT 'CREATE DATABASE airflow'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'airflow')\gexec
