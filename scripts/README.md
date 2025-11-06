# Scripts de Generación de Datos Sintéticos

Esta carpeta contiene scripts para generar datos sintéticos de movilidad académica internacional, útiles para ampliar el dataset cuando los datos reales son insuficientes.

## 📁 Scripts Disponibles

### 1. `generar_datos_sinteticos.py`
Genera datos sintéticos de **estudiantes internacionales** viniendo a Colombia.

**Características:**
- ✅ 500 registros sintéticos por defecto
- ✅ Distribución realista de países (México 30%, España 20%, Brasil 15%, etc.)
- ✅ Tipos de movilidad: Curso corto, Pasantía, Intercambio, Investigación, etc.
- ✅ Duraciones coherentes según tipo de movilidad
- ✅ Financiación calculada según país y duración
- ✅ Compatible con schema de `iush.csv`
- ✅ Combina automáticamente con datos reales si existen

**Archivos generados:**
- `data/raw/iush_sintetico.csv` - Solo datos sintéticos
- `data/raw/iush_completo.csv` - Datos reales + sintéticos

### 2. `generar_datos_docentes_sinteticos.py`
Genera datos sintéticos de **docentes internacionales** viniendo a Colombia.

**Características:**
- ✅ 200 registros sintéticos por defecto
- ✅ Distribución realista de países (España 25%, México 20%, Argentina 15%, etc.)
- ✅ Tipos de movilidad: Docencia, Investigación, Capacitación, Conferencia, etc.
- ✅ Universidades receptoras: UdeA, IUSH, UNAC, Nacional
- ✅ Financiación mayor que estudiantes (más recursos para docentes)
- ✅ Compatible con schema de archivo de docentes
- ✅ Genera tanto CSV como Excel

**Archivos generados:**
- `data/raw/docentes_exterior_sintetico.csv` - Formato CSV
- `data/raw/docentes_exterior_sintetico.xlsx` - Formato Excel

## 🚀 Uso

### Generación Rápida

**Activar entorno virtual y ejecutar:**

```powershell
# Activar entorno virtual
.venv\Scripts\Activate.ps1

# Generar datos de estudiantes
python scripts\generar_datos_sinteticos.py

# Generar datos de docentes
python scripts\generar_datos_docentes_sinteticos.py
```

### Personalización

#### Cambiar número de registros:

Editar las variables en cada script:

```python
# En generar_datos_sinteticos.py
NUM_REGISTROS = 1000  # Cambiar a la cantidad deseada

# En generar_datos_docentes_sinteticos.py
NUM_REGISTROS = 500  # Cambiar a la cantidad deseada
```

#### Cambiar rango de años:

```python
AÑOS = [2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025]
```

#### Ajustar distribución de países:

```python
PAISES = {
    'MÉXICO': 0.35,      # Aumentar a 35%
    'ESPAÑA': 0.25,      # Aumentar a 25%
    'BRASIL': 0.20,      # etc.
    # ... más países
}
```

## 📊 Datos Generados

### Estudiantes Internacionales

**Columnas generadas:**
- `AÑO`, `SEMESTRE` - Información temporal (2020-2025)
- `ID_TIPO_DOCUMENTO`, `NUM_DOCUMENTO` - Identificación (ficticia)
- `PRIMER_NOMBRE`, `SEGUNDO_NOMBRE`, `PRIMER_APELLIDO`, `SEGUNDO_APELLIDO`
- `PAIS_EXTRANJERO`, `ID_PAIS_EXTRANJERO` - País de origen
- `INSTITUCION_EXTRANJERA` - Universidad de origen
- `TIPO_MOV_EST_EXTRANJ` - Tipo de movilidad
- `NUM_DIAS_MOVILIDAD` - Duración en días
- `VALOR_FINANCIACION_NACIONAL` - Financiación colombiana
- `VALOR_FINANCIACION_INTERNAC` - Financiación internacional
- Más campos según schema original...

**Distribución típica:**
- **Países:** México (30%), España (20%), Brasil (15%), Italia (12%), Grecia (10%)
- **Tipos:** Curso corto (60%), Pasantía (20%), Intercambio (10%), Investigación (5%)
- **Duración:** 3-180 días según tipo de movilidad
- **Financiación:** 300K-40M COP según país y duración

### Docentes Internacionales

**Columnas generadas:**
- Similar a estudiantes, con campos específicos:
- `TIPO_MOV_DOC_EXTRANJ` - Tipo de movilidad de docentes
- `UNIVERSIDAD` - Universidad colombiana receptora
- Financiación generalmente mayor que estudiantes

**Distribución típica:**
- **Países:** España (25%), México (20%), Argentina (15%), Brasil (12%)
- **Tipos:** Docencia (40%), Investigación (30%), Capacitación (15%)
- **Universidades:** UdeA, IUSH, UNAC, Nacional (distribuidas equitativamente)
- **Duración:** 3-90 días según tipo de movilidad

## 🔄 Integración con Pipeline

Los datos sintéticos se integran automáticamente con el pipeline:

### Opción 1: Usar solo datos sintéticos

```python
# En notebook 01 o 02
df = pd.read_csv(DATA_RAW_DIR / 'iush_sintetico.csv')
df_docentes = pd.read_csv(DATA_RAW_DIR / 'docentes_exterior_sintetico.csv')
```

### Opción 2: Usar datos combinados (reales + sintéticos)

```python
# El script genera automáticamente iush_completo.csv
df = pd.read_csv(DATA_RAW_DIR / 'iush_completo.csv')
```

### Opción 3: Integración con sistema flexible de carga (Notebook 02)

El sistema de carga flexible del notebook 02 detecta automáticamente todos los archivos:

```python
# Configurar en config/column_mappings.json
{
  "sources": {
    "iush_sintetico": { ... },
    "docentes_sintetico": { ... }
  }
}

# El sistema cargará y consolidará automáticamente
```

## 📈 Estadísticas de Generación

Los scripts muestran estadísticas automáticamente:

```
ESTADÍSTICAS DEL DATASET SINTÉTICO
================================================================================

Total de registros: 500

📅 Distribución temporal:
               Registros
AÑO  SEMESTRE
2020 1                33
     2                36
2021 1                30
...

🌍 Top 10 países:
MÉXICO                       177
ESPAÑA                        88
BRASIL                        80
...

🎓 Tipos de movilidad:
Curso corto              299
Pasantía                  92
...

💰 Estadísticas financieras:
mean     6.177665e+06
std      7.491790e+06
...
```

## ⚙️ Configuración Avanzada

### Seed para reproducibilidad:

```python
# Cambiar seed para diferentes datasets
np.random.seed(123)  # Usa cualquier número
random.seed(123)
```

### Agregar nuevos países:

```python
PAISES = {
    'MÉXICO': 0.30,
    'TU_NUEVO_PAIS': 0.05,  # Agregar aquí
    # Asegurar que sumen 1.0
}

INSTITUCIONES = {
    'TU_NUEVO_PAIS': ['Universidad A', 'Universidad B'],
}
```

### Agregar nuevos tipos de movilidad:

```python
TIPOS_MOVILIDAD = {
    'Curso corto': 0.60,
    'TU_NUEVO_TIPO': 0.05,  # Agregar aquí
    # Ajustar para que sume 1.0
}

DURACIONES = {
    'TU_NUEVO_TIPO': (min_dias, max_dias),
}
```

## 🎯 Casos de Uso

### 1. Dataset insuficiente
Si tienes < 100 registros reales, genera 500-1000 sintéticos para análisis robusto.

### 2. Proyecciones futuras
Genera datos para años futuros (2026, 2027) y compara con proyecciones de modelos.

### 3. Testing
Usa datos sintéticos para probar el pipeline antes de usar datos reales sensibles.

### 4. Validación de modelos
Genera múltiples datasets sintéticos y verifica que tus modelos funcionen consistentemente.

## ⚠️ Consideraciones

1. **Los datos son ficticios** - No representan personas o instituciones reales
2. **Distribuciones aproximadas** - Basadas en patrones observados en datos reales
3. **Para análisis académico** - No usar para decisiones que requieran datos reales
4. **Combinar con datos reales** - Los sintéticos complementan, no reemplazan datos reales
5. **Semilla fija** - Regenerar el mismo script produce los mismos datos (reproducibilidad)

## 📝 Notas

- Los nombres y documentos son completamente ficticios
- Las financiaciones se calculan con fórmulas realistas basadas en país y duración
- Las distribuciones de probabilidad están calibradas con datos reales del IUSH
- Los scripts son compatibles con el sistema de mapeo de columnas del proyecto

## 🔗 Referencias

- `config/column_mappings.json` - Schema de columnas canónicas
- `notebooks/01_carga_exploracion_datos.ipynb` - Carga de datos
- `notebooks/02_limpieza_estandarizacion_etl.ipynb` - Procesamiento con sistema flexible
