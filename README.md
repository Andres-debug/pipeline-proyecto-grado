# Proyecto de Grado: Arquitectura de BI y Big Data para Turismo Académico en Medellín

## Descripción del Proyecto

Este proyecto implementa un sistema integral de Inteligencia de Negocios y Big Data orientado al análisis del impacto económico del turismo académico en la ciudad de Medellín. El sistema consolida datos de movilidad estudiantil internacional provenientes de tres instituciones universitarias: IUSH, Universidad de Antioquia y UNAC.

La arquitectura desarrollada permite transformar datos fragmentados y heterogéneos en información estratégica para la toma de decisiones en el sector educativo y turístico de la región.

---

## Objetivos

El proyecto busca alcanzar los siguientes objetivos específicos:

1. Consolidar datos dispersos de las oficinas de internacionalización de las universidades participantes
2. Desarrollar un pipeline ETL automatizado utilizando Python y sus librerías especializadas
3. Implementar modelos estadísticos descriptivos y predictivos (ARIMA, regresión lineal, machine learning)
4. Crear visualizaciones interactivas mediante dashboards en Power BI
5. Cuantificar el impacto económico directo e indirecto del turismo académico en Medellín

---

## Estructura del Proyecto

```
proyecto_turismo_academico/
│
├── notebooks/                              # Jupyter Notebooks del pipeline
│   ├── 01_carga_exploracion_datos.ipynb   # Carga y exploración inicial
│   ├── 02_limpieza_estandarizacion_etl.ipynb  # Limpieza y ETL
│   ├── 03_analisis_descriptivo.ipynb      # Análisis estadístico completo
│   ├── 04_modelos_predictivos.ipynb       # Modelos ARIMA y ML
│   └── 05_integracion_powerbi_exportacion.ipynb  # Preparación para Power BI
│
├── data/
│   ├── raw/                               # Datos crudos originales
│   │   └── iush.csv                       # Datos IUSH (disponible)
│   ├── processed/                         # Datos limpios y procesados
│   │   ├── datos_consolidados_limpios.csv
│   │   └── datos_consolidados_limpios.xlsx
│   └── results/                           # Resultados y tablas finales
│       ├── dim_tiempo.csv                 # Dimensión temporal
│       ├── dim_geografia.csv              # Dimensión países
│       ├── dim_universidad.csv            # Dimensión universidades
│       ├── dim_tipo_movilidad.csv         # Dimensión tipos movilidad
│       ├── fact_movilidad.csv             # Tabla de hechos
│       ├── kpis_powerbi.csv               # KPIs principales
│       └── proyecciones_arima.csv         # Proyecciones futuras
│
├── outputs/
│   ├── graficas/                          # Visualizaciones generadas
│   │   ├── 01_exploracion_inicial_iush.png
│   │   ├── 03_analisis_temporal.png
│   │   ├── 03_analisis_geografico.png
│   │   ├── 04_proyecciones_arima.png
│   │   └── ...
│   └── reportes/                          # Reportes y documentación
│       ├── reporte_calidad_datos.txt
│       ├── reporte_modelos.md
│       ├── guia_powerbi.txt
│       └── reporte_ejecutivo_final.md
│
├── sql/
│   └── crear_tablas_postgresql.sql        # Script de creación BD
│
├── .gitignore                             # Archivos ignorados por Git
├── requirements.txt                        # Dependencias Python
└── README.md                              # Este archivo
```

---

## Instalación y Configuración

### Prerrequisitos

El proyecto requiere las siguientes herramientas instaladas en el sistema:

- Python 3.10 o superior
- Jupyter Notebook o JupyterLab
- PostgreSQL (opcional, para entornos de producción)
- Power BI Desktop (para visualizaciones finales)

### Paso 1: Preparación del Entorno

Navegue al directorio del proyecto:

```bash
cd C:\Users\Administrador\Desktop\Especializacion\pgrado-api
```

### Paso 2: Creación de Entorno Virtual

Se recomienda utilizar un entorno virtual para aislar las dependencias del proyecto:

```bash
# Crear entorno virtual
python -m venv .venv

# Activar entorno virtual
# En Windows PowerShell:
.venv\Scripts\Activate.ps1
# En Windows CMD:
.venv\Scripts\activate.bat
```

### Paso 3: Instalación de Dependencias

Instale todas las librerías necesarias mediante el archivo de requisitos:

```bash
pip install -r requirements.txt
```

El archivo `requirements.txt` incluye las siguientes librerías principales:

- pandas: manipulación y análisis de datos
- numpy: operaciones numéricas y matrices
- matplotlib y seaborn: visualización de datos
- statsmodels: modelos estadísticos y series temporales
- scikit-learn: algoritmos de machine learning
- openpyxl: lectura y escritura de archivos Excel
- psycopg2-binary: conexión a bases de datos PostgreSQL

---

## Uso del Sistema

### Ejecución Secuencial de Notebooks

Los notebooks deben ejecutarse en orden estricto, ya que cada uno genera archivos que son utilizados por los siguientes. A continuación se describe el propósito de cada notebook:

#### Notebook 1: Carga y Exploración de Datos

```bash
jupyter notebook notebooks/01_carga_exploracion_datos.ipynb
```

Este notebook realiza las siguientes operaciones:

- Carga inicial de archivos CSV provenientes de IUSH
- Inspección de dimensiones, tipos de datos y estructura general
- Identificación preliminar de problemas de calidad (valores nulos, duplicados, inconsistencias)
- Generación de visualizaciones exploratorias básicas

Salida: Gráficas preliminares guardadas en `outputs/graficas/`

---

#### Notebook 2: Limpieza y ETL

```bash
jupyter notebook notebooks/02_limpieza_estandarizacion_etl.ipynb
```

Funciones principales:

- Eliminación de filas completamente vacías y duplicados
- Estandarización de nomenclatura de países según códigos ISO
- Creación de variables derivadas (periodo académico, categorías de duración, etc.)
- Validación de calidad posterior a la limpieza
- Exportación de datos limpios

Salida: Archivo `data/processed/datos_consolidados_limpios.csv`

---

#### Notebook 3: Análisis Descriptivo

```bash
jupyter notebook notebooks/03_analisis_descriptivo.ipynb
```

Análisis realizados:

- Estadísticas descriptivas completas (media, mediana, desviación estándar, percentiles)
- Análisis de series temporales: tendencias, estacionalidad, tasas de crecimiento
- Distribución geográfica: principales países de origen y evolución temporal
- Análisis por tipo de movilidad y duración de estancia
- Estimación de impacto económico basado en modelos de gasto promedio
- Detección de valores atípicos mediante método IQR
- Análisis de correlaciones entre variables

Salida: 
- Múltiples visualizaciones en `outputs/graficas/`
- Archivo `data/results/estadisticas_descriptivas.csv`

---

#### Notebook 4: Modelos Predictivos

```bash
jupyter notebook notebooks/04_modelos_predictivos.ipynb
```

Modelos implementados:

- **ARIMA (AutoRegressive Integrated Moving Average)**: proyecciones de flujos futuros de movilidad estudiantil para los próximos 6 semestres académicos
- **Regresión Lineal Múltiple**: identificación de variables explicativas de la duración de movilidad
- **Random Forest**: modelo de comparación para validar precisión predictiva
- **Estimación de impacto económico futuro**: proyecciones de gasto con multiplicador económico

Métricas de evaluación: R², RMSE, MAE, MAPE

Salida:
- `data/results/proyecciones_arima.csv`
- `data/results/proyecciones_impacto_economico.csv`
- `data/results/comparacion_modelos.csv`
- `outputs/reportes/reporte_modelos.md`

---

#### Notebook 5: Integración con Power BI

```bash
jupyter notebook notebooks/05_integracion_powerbi_exportacion.ipynb
```

Procesos ejecutados:

- Diseño e implementación de modelo dimensional (esquema estrella)
- Creación de tablas de dimensiones: tiempo, geografía, universidad, tipo de movilidad
- Creación de tabla de hechos con métricas de movilidad
- Cálculo de 11 KPIs principales para dashboards
- Generación de script SQL para PostgreSQL
- Exportación de datos optimizados para Power BI

Salida:
- Modelo dimensional completo en `data/results/`
- Script SQL en `sql/crear_tablas_postgresql.sql`
- Guía de integración en `outputs/reportes/guia_powerbi.txt`
- Reporte ejecutivo final en `outputs/reportes/reporte_ejecutivo_final.md`

---

## Integración con Power BI

### Opción 1: Importación desde Archivos CSV

Esta opción es la más rápida y recomendada para desarrollo:

1. Abra Power BI Desktop
2. Seleccione **Inicio > Obtener datos > Texto/CSV**
3. Importe los siguientes archivos desde `data/results/`:
   - dim_tiempo.csv
   - dim_geografia.csv
   - dim_universidad.csv
   - dim_tipo_movilidad.csv
   - fact_movilidad.csv
4. En la **Vista de Modelo**, establezca las siguientes relaciones:
   - fact_movilidad[ID_TIEMPO] → dim_tiempo[ID_TIEMPO]
   - fact_movilidad[ID_PAIS] → dim_geografia[ID_PAIS]
   - fact_movilidad[ID_UNIVERSIDAD] → dim_universidad[ID_UNIVERSIDAD]
   - fact_movilidad[ID_TIPO_MOVILIDAD] → dim_tipo_movilidad[ID_TIPO_MOVILIDAD]

### Opción 2: Conexión a PostgreSQL

Para entornos de producción se recomienda utilizar una base de datos relacional:

1. Instale PostgreSQL en su sistema
2. Ejecute el script de creación de base de datos:
   ```bash
   psql -U postgres -f sql/crear_tablas_postgresql.sql
   ```
3. Cargue los datos CSV en las tablas correspondientes
4. En Power BI Desktop: **Obtener datos > PostgreSQL**
5. Ingrese las credenciales y seleccione la base de datos `turismo_academico_medellin`

Para mayor detalle, consulte la guía completa en `outputs/reportes/guia_powerbi.txt`

---

## Indicadores Clave de Desempeño (KPIs)

El sistema calcula los siguientes KPIs principales:

| Indicador | Descripción |
|-----------|-------------|
| Total Estudiantes | Cantidad acumulada de estudiantes internacionales |
| Países Representados | Número de países de origen únicos |
| Duración Promedio | Media de días de estadía por estudiante |
| Impacto Económico Total | Estimación de gasto directo e indirecto (con multiplicador) |
| Tasa de Crecimiento Anual | Variación porcentual interanual de llegadas |
| Top 10 Países | Principales países de origen por volumen |

---

## Modelos Analíticos Implementados

### 1. Modelo ARIMA

- **Propósito**: Proyección de series temporales de movilidad estudiantil
- **Configuración**: ARIMA(p=1, d=1, q=1)
- **Horizonte temporal**: 6 periodos académicos (3 años)
- **Métricas de evaluación**: RMSE, MAE, MAPE

### 2. Regresión Lineal Múltiple

- **Propósito**: Identificación de factores determinantes de la duración de movilidad
- **Variables independientes**: Año, semestre, país de origen, tipo de movilidad, fuente de financiación
- **Métricas**: Coeficiente de determinación (R²), RMSE, MAE

### 3. Random Forest

- **Propósito**: Modelo de contraste para validación de precisión
- **Configuración**: 100 árboles de decisión, profundidad máxima de 10 niveles
- **Output adicional**: Ranking de importancia de características

---

## Visualizaciones Generadas

El sistema genera automáticamente más de 10 visualizaciones de calidad académica:

- Evolución temporal de movilidad (serie de tiempo)
- Distribución geográfica por país (gráfico de barras y mapas)
- Análisis de impacto económico por periodo
- Comparación entre universidades
- Proyecciones futuras ARIMA con intervalos de confianza
- Matriz de correlaciones
- Boxplots para detección de outliers

Todas las gráficas se guardan en formato PNG con resolución de 300 DPI en el directorio `outputs/graficas/`.

---

## Solución de Problemas Comunes

### Error: ModuleNotFoundError

Si aparece un error indicando que falta un módulo de Python:

```bash
pip install -r requirements.txt --upgrade
```

### Error: FileNotFoundError

Verifique que el archivo de datos esté ubicado en `data/raw/iush.csv`. Asegúrese de que la estructura de carpetas sea correcta.

### Jupyter Notebook no inicia

Reinstale Jupyter:

```bash
pip install jupyter --upgrade
jupyter notebook
```

### Problemas de codificación de caracteres

Los archivos CSV utilizan codificación UTF-8. Si encuentra problemas al leer archivos:

```python
df = pd.read_csv('archivo.csv', encoding='utf-8-sig')
```

---

## Notas Importantes

**Estado actual de los datos**: En la versión actual del proyecto, solo se cuenta con datos de la institución IUSH. Los datos de la Universidad de Antioquia y UNAC se integrarán una vez estén disponibles mediante las oficinas de internacionalización correspondientes.

**Limitaciones de las proyecciones**: Los modelos ARIMA se basan en datos históricos limitados. La precisión de las proyecciones mejorará significativamente con la incorporación de series temporales más extensas.

**Estimaciones económicas**: Los cálculos de impacto económico utilizan un gasto promedio estimado de $50 USD por día, basado en estudios de referencia sobre turismo educativo internacional. Se aplica un multiplicador económico de 1.8x para contabilizar el efecto indirecto en la economía local.

---

## Documentación Complementaria

El proyecto incluye documentación detallada adicional:

- **Guía de integración Power BI**: `outputs/reportes/guia_powerbi.txt`
- **Reporte ejecutivo final**: `outputs/reportes/reporte_ejecutivo_final.md`
- **Documentación de modelos**: `outputs/reportes/reporte_modelos.md`
- **Reporte de calidad de datos**: `outputs/reportes/reporte_calidad_datos.txt`

---

## Información del Proyecto

**Proyecto de Grado - Especialización en Inteligencia de Negocios y Big Data**  
Institución: [Nombre de la Universidad]  
Fecha: Octubre 2025

---

## Licencia

Este proyecto tiene fines académicos y de investigación sobre el impacto del turismo académico en Medellín.

---

## Agradecimientos

Se agradece especialmente a:

- IUSH por facilitar los datos de movilidad estudiantil
- Universidad de Antioquia y UNAC por su colaboración futura
- Comunidades de desarrollo de Python, Pandas, Scikit-learn y demás librerías de código abierto

---

## Próximos Pasos

1. Ejecutar los 5 notebooks en secuencia
2. Importar el modelo dimensional en Power BI
3. Integrar datos de Universidad de Antioquia y UNAC cuando estén disponibles
4. Implementar sistema de actualización automática semestral
5. Presentar resultados a stakeholders y oficinas de internacionalización

---

## 📊 Datos Sintéticos

El proyecto incluye un sistema de generación de datos sintéticos para ampliar el dataset disponible:

### Archivos de Datos Disponibles

**Estudiantes:**
- `data/raw/iush.csv` - 27 registros reales
- `data/raw/iush_sintetico.csv` - 500 registros sintéticos
- `data/raw/iush_completo.csv` - 527 registros (reales + sintéticos) ✅ **Recomendado**

**Docentes:**
- `data/raw/docentes_exterior_sintetico.csv` - 200 registros sintéticos
- `data/raw/docentes_exterior_sintetico.xlsx` - 200 registros sintéticos (Excel)

### Generar Nuevos Datos Sintéticos

Si necesitas más datos o diferentes distribuciones:

```bash
# Activar entorno virtual
.venv\Scripts\Activate.ps1

# Generar todos los datos sintéticos
python scripts\generar_todos_datos_sinteticos.py

# O generar individualmente
python scripts\generar_datos_sinteticos.py          # Estudiantes
python scripts\generar_datos_docentes_sinteticos.py # Docentes
```

**Consultar:** `scripts/README.md` para personalización avanzada (cantidad de registros, países, años, etc.)

---

**Para iniciar el proyecto, ejecute:**

```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. (Opcional) Generar datos sintéticos adicionales
python scripts\generar_todos_datos_sinteticos.py

# 3. Iniciar análisis
jupyter notebook notebooks/01_carga_exploracion_datos.ipynb
```

**Nota:** El Notebook 02 está configurado para usar `iush_completo.csv` (datos reales + sintéticos) por defecto.
