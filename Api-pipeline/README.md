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

La integración con BD quedó preparada para conectarla después vía `DB_URL`.
Cuando la base esté lista, agregamos la capa de carga con SQLAlchemy o psycopg2.
