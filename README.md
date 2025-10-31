# 🎓 Proyecto de Grado: Arquitectura de BI y Big Data para Turismo Académico en Medellín

## 📋 Descripción del Proyecto

Sistema completo de Inteligencia de Negocios y Big Data para analizar el impacto económico del turismo académico en Medellín, consolidando datos de movilidad estudiantil internacional de tres universidades: **IUSH**, **Universidad de Antioquia** y **UNAC**.

---

## 🎯 Objetivos

1. ✅ Consolidar datos fragmentados de oficinas de internacionalización
2. ✅ Crear pipeline ETL automatizado en Python
3. ✅ Implementar modelos descriptivos y predictivos (ARIMA, regresión, ML)
4. ✅ Desarrollar dashboards en Power BI
5. ✅ Cuantificar el impacto económico del turismo académico

---

## 🗂️ Estructura del Proyecto

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
├── requirements.txt                        # Dependencias Python
└── README.md                              # Este archivo
```

---

## 🚀 Instalación y Configuración

### Prerrequisitos

- **Python 3.10+** instalado
- **Jupyter Notebook** o **JupyterLab**
- **PostgreSQL** (opcional, para producción)
- **Power BI Desktop** (para visualizaciones finales)

### Paso 1: Clonar o Descargar el Proyecto

```bash
cd C:\Users\Administrador\Desktop\Especializacion\pgrado-api
```

### Paso 2: Crear Entorno Virtual (Recomendado)

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# En Windows:
venv\Scripts\activate
# En Linux/Mac:
source venv/bin/activate
```

### Paso 3: Instalar Dependencias

```bash
pip install -r requirements.txt
```

**Librerías principales incluidas:**
- `pandas` - Manipulación de datos
- `numpy` - Cálculos numéricos
- `matplotlib`, `seaborn` - Visualizaciones
- `statsmodels` - Modelos ARIMA
- `scikit-learn` - Machine Learning
- `openpyxl` - Lectura/escritura Excel
- `psycopg2-binary` - Conexión PostgreSQL

---

## 📊 Uso del Sistema

### Ejecución Secuencial de Notebooks

Los notebooks deben ejecutarse **en orden** ya que cada uno depende del anterior:

#### **Notebook 1: Carga y Exploración**
```bash
jupyter notebook notebooks/01_carga_exploracion_datos.ipynb
```

**Qué hace:**
- ✅ Carga datos CSV de IUSH
- ✅ Inspecciona dimensiones y estructura
- ✅ Identifica problemas de calidad
- ✅ Genera visualizaciones preliminares

**Salida:** Gráficas exploratorias en `outputs/graficas/`

---

#### **Notebook 2: Limpieza y ETL**
```bash
jupyter notebook notebooks/02_limpieza_estandarizacion_etl.ipynb
```

**Qué hace:**
- ✅ Elimina filas vacías y duplicados
- ✅ Estandariza nomenclatura de países
- ✅ Crea variables derivadas (periodo, categorías, etc.)
- ✅ Valida calidad post-limpieza

**Salida:** `data/processed/datos_consolidados_limpios.csv`

---

#### **Notebook 3: Análisis Descriptivo**
```bash
jupyter notebook notebooks/03_analisis_descriptivo.ipynb
```

**Qué hace:**
- ✅ Estadísticas descriptivas completas
- ✅ Análisis temporal de tendencias
- ✅ Distribución geográfica de estudiantes
- ✅ Análisis financiero
- ✅ Identificación de outliers
- ✅ Matriz de correlaciones

**Salida:** 
- Gráficas de análisis en `outputs/graficas/`
- `data/results/estadisticas_descriptivas.csv`

---

#### **Notebook 4: Modelos Predictivos**
```bash
jupyter notebook notebooks/04_modelos_predictivos.ipynb
```

**Qué hace:**
- ✅ Modelo ARIMA para proyecciones temporales
- ✅ Modelo de Regresión Lineal
- ✅ Modelo Random Forest (comparación)
- ✅ Estimación de impacto económico futuro

**Salida:**
- `data/results/proyecciones_arima.csv`
- `data/results/proyecciones_impacto_economico.csv`
- `data/results/comparacion_modelos.csv`
- `outputs/reportes/reporte_modelos.md`

---

#### **Notebook 5: Integración Power BI**
```bash
jupyter notebook notebooks/05_integracion_powerbi_exportacion.ipynb
```

**Qué hace:**
- ✅ Crea modelo dimensional (esquema estrella)
- ✅ Genera tablas dim_* y fact_movilidad
- ✅ Calcula KPIs principales
- ✅ Exporta datos optimizados para Power BI
- ✅ Genera script SQL para PostgreSQL

**Salida:**
- Modelo dimensional completo en `data/results/`
- `sql/crear_tablas_postgresql.sql`
- `outputs/reportes/guia_powerbi.txt`
- `outputs/reportes/reporte_ejecutivo_final.md`

---

## 📈 Integración con Power BI

### Opción 1: Importar desde CSV (Rápido)

1. Abrir **Power BI Desktop**
2. **Inicio** > **Obtener datos** > **Texto/CSV**
3. Importar archivos desde `data/results/`:
   - `dim_tiempo.csv`
   - `dim_geografia.csv`
   - `dim_universidad.csv`
   - `dim_tipo_movilidad.csv`
   - `fact_movilidad.csv`
4. En **Vista de Modelo**, crear relaciones:
   - `fact_movilidad[ID_TIEMPO]` → `dim_tiempo[ID_TIEMPO]`
   - `fact_movilidad[ID_PAIS]` → `dim_geografia[ID_PAIS]`
   - `fact_movilidad[ID_UNIVERSIDAD]` → `dim_universidad[ID_UNIVERSIDAD]`
   - `fact_movilidad[ID_TIPO_MOVILIDAD]` → `dim_tipo_movilidad[ID_TIPO_MOVILIDAD]`

### Opción 2: Usar PostgreSQL (Producción)

1. Instalar PostgreSQL
2. Ejecutar script:
   ```bash
   psql -U postgres -f sql/crear_tablas_postgresql.sql
   ```
3. Cargar datos CSV en PostgreSQL
4. En Power BI: **Obtener datos** > **PostgreSQL**
5. Conectar a base de datos `turismo_academico_medellin`

**Guía completa:** Ver `outputs/reportes/guia_powerbi.txt`

---

## 🎯 KPIs Principales

| KPI | Descripción |
|-----|-------------|
| **Total Estudiantes** | Cantidad total de estudiantes internacionales |
| **Países Representados** | Número de países de origen únicos |
| **Duración Promedio** | Promedio de días de estadía |
| **Impacto Económico Total** | Gasto estimado total (directo + multiplicador) |
| **Tasa de Crecimiento** | Variación interanual de estudiantes |
| **Top Países** | Principales 10 países de origen |

---

## 🔍 Modelos Implementados

### 1. **Modelo ARIMA**
- **Propósito:** Proyección de flujos futuros de movilidad
- **Parámetros:** (p=1, d=1, q=1)
- **Métricas:** RMSE, MAE, MAPE
- **Horizonte:** 3 años (6 semestres)

### 2. **Regresión Lineal**
- **Propósito:** Identificar variables influyentes en duración de movilidad
- **Variables:** Año, Semestre, País, Tipo de movilidad, Financiación
- **Métricas:** R², RMSE, MAE

### 3. **Random Forest**
- **Propósito:** Comparación de precisión predictiva
- **Parámetros:** 100 árboles, profundidad máxima 10
- **Output:** Importancia de características

---

## 📊 Visualizaciones Generadas

El sistema genera automáticamente más de 10 gráficas profesionales:

- 📈 Evolución temporal de movilidad
- 🌍 Distribución geográfica por país
- 💰 Análisis de impacto económico
- 📊 Comparación por universidad
- 🔮 Proyecciones futuras ARIMA
- 📉 Análisis de correlaciones
- 🎯 Detección de outliers

Todas guardadas en `outputs/graficas/` en alta resolución (300 DPI).

---

## 🛠️ Solución de Problemas

### Error: "ModuleNotFoundError"
```bash
pip install -r requirements.txt --upgrade
```

### Error: "FileNotFoundError"
Verificar que los datos estén en `data/raw/iush.csv`

### Jupyter no inicia
```bash
pip install jupyter --upgrade
jupyter notebook
```

### Errores de codificación
Los archivos CSV usan codificación UTF-8. Si hay problemas:
```python
df = pd.read_csv('archivo.csv', encoding='utf-8-sig')
```

---

## 📝 Notas Importantes

⚠️ **Datos actuales:** Solo se tienen datos de IUSH. Los datos de Universidad de Antioquia y UNAC se integrarán cuando estén disponibles.

⚠️ **Proyecciones:** Las proyecciones ARIMA se basan en datos históricos limitados. Mayor cantidad de datos mejorará la precisión.

⚠️ **Impacto económico:** Los cálculos usan estimaciones de gasto promedio ($50 USD/día) basadas en estudios de turismo educativo.

---

## 📚 Documentación Adicional

- **Guía Power BI:** `outputs/reportes/guia_powerbi.txt`
- **Reporte Ejecutivo:** `outputs/reportes/reporte_ejecutivo_final.md`
- **Reporte de Modelos:** `outputs/reportes/reporte_modelos.md`
- **Calidad de Datos:** `outputs/reportes/reporte_calidad_datos.txt`

---

## 👥 Autor

**Proyecto de Grado - Especialización**  
Institución: [Tu Universidad]  
Fecha: Octubre 2025

---

## 📄 Licencia

Este proyecto es de uso académico para fines de investigación en turismo académico.

---

## 🙏 Agradecimientos

- IUSH por proporcionar los datos de movilidad estudiantil
- Universidad de Antioquia y UNAC (colaboración futura)
- Comunidad de Python y librerías de código abierto

---

## 🚀 Próximos Pasos

1. ✅ **Ejecutar los 5 notebooks en orden**
2. ✅ **Importar datos en Power BI**
3. ⏳ **Integrar datos de UdeA y UNAC cuando estén disponibles**
4. ⏳ **Automatizar actualización semestral**
5. ⏳ **Presentar resultados a stakeholders**

---

**¡Sistema listo para uso!** 🎉

Para comenzar:
```bash
pip install -r requirements.txt
jupyter notebook notebooks/01_carga_exploracion_datos.ipynb
```
