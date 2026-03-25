# API Pipeline - Turismo Académico

Proyecto FastAPI que migra el flujo ETL de los notebooks a una API ejecutable:

- Carga fuentes desde `data/raw`
- Normaliza esquema con `config/column_mappings.json`
- Limpia y estandariza datos
- Construye modelo dimensional para Power BI
- Exporta dimensiones, hechos y KPIs en `data/results`

## 1) Preparación

```powershell
cd Api-pipeline
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Crear archivo de entorno:

```powershell
Copy-Item .env.example .env
```

## 2) Ejecutar API

```powershell
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

## 3) Endpoints

- `GET /health`
- `GET /pipeline/status`
- `POST /pipeline/run`
- `GET /airflow/health`
- `GET /airflow/dags`
- `POST /airflow/dags/{dag_id}/runs`
- `GET /airflow/dags/{dag_id}/runs/{dag_run_id}`

Payload opcional de ejecución:

```json
{
  "iush_filename": "iush_completo.csv",
  "docentes_filename": "docentes_exterior_sintetico.csv"
}
```

## 4) Salidas generadas

- `data/processed/datos_consolidados_limpios.csv`
- `data/results/dim_tiempo.csv`
- `data/results/dim_geografia.csv`
- `data/results/dim_universidad.csv`
- `data/results/dim_tipo_movilidad.csv`
- `data/results/fact_movilidad.csv`
- `data/results/kpis_powerbi.csv`
- `outputs/reportes/reporte_calidad_datos_api.txt`

## 5) Base de datos (siguiente paso)

La API ahora usa SQLAlchemy ORM para crear automáticamente la base y tablas en PostgreSQL al iniciar.

Variables relevantes en `.env`:

- `DB_URL=postgresql+psycopg://usuario:password@host:puerto/base_datos`
- `DB_SCHEMA=public`

Comportamiento al iniciar `uvicorn`:

- Si la base de datos no existe, intenta crearla.
- Crea el esquema si no existe (`DB_SCHEMA`).
- Crea tablas del modelo estrella y `kpis_movilidad` si no existen.

Luego, al ejecutar `POST /pipeline/run`, la API trunca las tablas y vuelve a cargar datos manteniendo estructura ORM (sin `replace`).

## 6) Migraciones con Alembic

Instalar dependencias y aplicar migración inicial:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m alembic upgrade head
```

Si las tablas ya existen (porque la API las creó antes), registra baseline:

```powershell
.\.venv\Scripts\python.exe -m alembic stamp head
.\.venv\Scripts\python.exe -m alembic current
```

Crear una nueva migración automática después de cambios en modelos:

```powershell
.\.venv\Scripts\python.exe -m alembic revision --autogenerate -m "descripcion_cambio"
.\.venv\Scripts\python.exe -m alembic upgrade head
```

## 7) Integración Airflow (desde FastAPI)

Variables en `.env` para Airflow:

- `AIRFLOW_API_BASE_URL=http://localhost:8080`
- `AIRFLOW_USERNAME=airflow`
- `AIRFLOW_PASSWORD=airflow`
- `AIRFLOW_TIMEOUT_SECONDS=30`
- `AIRFLOW_VERIFY_SSL=false`

Notas:

- La API usa el endpoint REST de Airflow (`/api/v1`).
- Si `AIRFLOW_API_BASE_URL` no está configurado, los endpoints de Airflow responden que no está configurado.
- Puedes disparar DAGs desde Swagger en `/docs` usando `POST /airflow/dags/{dag_id}/runs`.
