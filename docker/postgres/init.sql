-- Script ejecutado una sola vez al inicializar el contenedor de PostgreSQL.
-- Crea las bases de datos para la API y para Airflow si no existen.

SELECT 'CREATE DATABASE pipeline'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'pipeline')\gexec

SELECT 'CREATE DATABASE airflow'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'airflow')\gexec
