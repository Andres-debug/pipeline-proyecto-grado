# 📊 Datos Sintéticos Generados - Resumen

## ✅ Generación Completada Exitosamente

Se han generado datos sintéticos realistas para ampliar el dataset del proyecto de movilidad académica internacional.

---

## 📁 Archivos Disponibles en `data/raw/`

### Estudiantes Internacionales

| Archivo | Descripción | Registros | Formato |
|---------|-------------|-----------|---------|
| `iush.csv` | Datos reales originales | 27 | CSV |
| `iush_sintetico.csv` | Solo datos sintéticos generados | 500 | CSV |
| `iush_completo.csv` | **Datos reales + sintéticos** | **527** | CSV |

### Docentes Internacionales

| Archivo | Descripción | Registros | Formato |
|---------|-------------|-----------|---------|
| `2. Movilidad_de_docentes_del_exterior_hacia_colombia.xlsx` | Datos reales originales | - | Excel |
| `docentes_exterior_sintetico.csv` | Datos sintéticos generados | 200 | CSV |
| `docentes_exterior_sintetico.xlsx` | Datos sintéticos generados | 200 | Excel |

---

## 📈 Estadísticas de Datos Sintéticos

### Estudiantes (500 registros sintéticos)

#### Distribución Temporal
- **Años:** 2020-2025 (6 años)
- **Semestres:** 1 y 2 distribuidos equitativamente
- **Promedio:** ~83 estudiantes por año

#### Top 5 Países de Origen
1. 🇲🇽 **México** - 177 estudiantes (35.4%)
2. 🇪🇸 **España** - 88 estudiantes (17.6%)
3. 🇧🇷 **Brasil** - 80 estudiantes (16.0%)
4. 🇮🇹 **Italia** - 52 estudiantes (10.4%)
5. 🇬🇷 **Grecia** - 43 estudiantes (8.6%)

#### Tipos de Movilidad
1. **Curso corto** - 299 (59.8%)
2. **Pasantía** - 92 (18.4%)
3. **Intercambio académico** - 57 (11.4%)
4. **Investigación** - 29 (5.8%)
5. **Conferencia** - 12 (2.4%)
6. **Workshop** - 11 (2.2%)

#### Duración
- **Promedio:** 38.4 días
- **Mínimo:** 3 días
- **Máximo:** 180 días
- **Mediana:** 13 días

#### Impacto Económico
- **Financiación promedio:** $6,177,665 COP
- **Rango:** $363,811 - $39,286,420 COP
- **Total estimado:** ~$3,088,832,500 COP

### Docentes (200 registros sintéticos)

#### Distribución Temporal
- **Años:** 2020-2025 (6 años)
- **Promedio:** ~33 docentes por año

#### Top 5 Países de Origen
1. 🇪🇸 **España** - 49 docentes (24.5%)
2. 🇲🇽 **México** - 42 docentes (21.0%)
3. 🇧🇷 **Brasil** - 27 docentes (13.5%)
4. 🇦🇷 **Argentina** - 23 docentes (11.5%)
5. 🇨🇱 **Chile** - 21 docentes (10.5%)

#### Tipos de Movilidad
1. **Docencia** - 84 (42.0%)
2. **Investigación** - 58 (29.0%)
3. **Capacitación** - 30 (15.0%)
4. **Conferencia** - 19 (9.5%)
5. **Asesoría académica** - 9 (4.5%)

#### Universidades Receptoras
- Universidad de Antioquia
- IUSH
- UNAC
- Universidad Nacional

#### Duración
- **Promedio:** 36.2 días
- **Rango:** 3-88 días

#### Impacto Económico
- **Financiación promedio:** $6,791,650 COP
- **Total estimado:** ~$1,358,330,000 COP

---

## 🎯 Dataset Combinado Total

### Resumen General

| Categoría | Estudiantes | Docentes | **Total** |
|-----------|-------------|----------|-----------|
| Datos reales | 27 | - | 27 |
| Datos sintéticos | 500 | 200 | 700 |
| **TOTAL** | **527** | **200** | **727** |

### Impacto Económico Total Estimado
- **Estudiantes:** ~$3,088,832,500 COP
- **Docentes:** ~$1,358,330,000 COP
- **TOTAL:** ~**$4,447,162,500 COP** (~$1,111,790 USD)

---

## 🚀 Próximos Pasos

### 1. Usar Dataset Completo (Recomendado)

```python
# En notebook 01 o 02
import pandas as pd
from pathlib import Path

DATA_RAW_DIR = BASE_DIR / 'data' / 'raw'

# Cargar datos combinados de estudiantes
df_estudiantes = pd.read_csv(DATA_RAW_DIR / 'iush_completo.csv')

# Cargar datos de docentes
df_docentes = pd.read_csv(DATA_RAW_DIR / 'docentes_exterior_sintetico.csv')
# o
df_docentes = pd.read_excel(DATA_RAW_DIR / 'docentes_exterior_sintetico.xlsx')
```

### 2. Ejecutar Pipeline Completo

```bash
# Activar entorno virtual
.venv\Scripts\Activate.ps1

# Ejecutar notebooks en orden
jupyter notebook notebooks/01_carga_exploracion_datos.ipynb
jupyter notebook notebooks/02_limpieza_estandarizacion_etl.ipynb
jupyter notebook notebooks/03_analisis_descriptivo.ipynb
jupyter notebook notebooks/04_modelos_predictivos.ipynb
jupyter notebook notebooks/05_integracion_powerbi_exportacion.ipynb
```

### 3. Sistema de Carga Flexible

El notebook 02 tiene un sistema que detecta y consolida automáticamente todos los archivos:

```python
# El sistema cargará automáticamente:
# - iush_completo.csv (527 registros)
# - docentes_exterior_sintetico.csv (200 registros)
# - Cualquier otro archivo en data/raw/

# Total consolidado: 727+ registros
```

---

## 📋 Ventajas de Usar Datos Sintéticos

✅ **Dataset robusto:** De 27 a 727 registros (aumento de 2,596%)
✅ **Análisis temporal:** 6 años de datos (2020-2025)
✅ **Distribución realista:** Basada en patrones de datos reales
✅ **Múltiples países:** 10+ países representados
✅ **Tipos variados:** 6 tipos de movilidad estudiantil + 5 docentes
✅ **Modelos predictivos:** Suficientes datos para ARIMA, Regresión, Random Forest
✅ **Reproducibilidad:** Seed fija permite regenerar datos idénticos
✅ **Privacidad:** Datos ficticios, sin información sensible

---

## ⚙️ Regenerar Datos

Si necesitas más datos o diferentes distribuciones:

```bash
# Regenerar todo
python scripts\generar_todos_datos_sinteticos.py

# Solo estudiantes
python scripts\generar_datos_sinteticos.py

# Solo docentes
python scripts\generar_datos_docentes_sinteticos.py
```

### Personalizar cantidad:

Editar en el script correspondiente:

```python
NUM_REGISTROS = 1000  # Cambiar según necesidad
AÑOS = [2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025]
```

---

## 📊 Calidad de Datos

### Validaciones Automáticas

Los datos sintéticos incluyen:

- ✅ Fechas coherentes (2020-2025, semestres 1-2)
- ✅ Países con códigos ISO correctos
- ✅ Duraciones realistas según tipo de movilidad
- ✅ Financiaciones calculadas según país y duración
- ✅ Instituciones reales de cada país
- ✅ Distribuciones de probabilidad calibradas
- ✅ Sin valores nulos en campos críticos
- ✅ Formatos compatibles con sistema de mapeo de columnas

---

## 🎓 Uso Académico

### Para el Proyecto

Los datos sintéticos son perfectos para:

1. **Desarrollo del pipeline ETL** - Probar transformaciones
2. **Modelos predictivos** - Entrenar y validar algoritmos
3. **Visualizaciones** - Crear gráficos y dashboards
4. **Documentación** - Ejemplos y screenshots
5. **Presentaciones** - Demostrar capacidades del sistema

### Nota Importante

⚠️ Los datos sintéticos **complementan** pero **no reemplazan** datos reales
⚠️ Para decisiones empresariales, usar solo datos reales validados
⚠️ Indicar claramente en reportes qué datos son sintéticos

---

## 📞 Soporte

Para regenerar datos con diferentes parámetros, consultar:
- `scripts/README.md` - Documentación completa
- `scripts/generar_datos_sinteticos.py` - Código fuente estudiantes
- `scripts/generar_datos_docentes_sinteticos.py` - Código fuente docentes

---

**Fecha de generación:** 2025-11-05
**Total de registros sintéticos:** 700
**Estado:** ✅ Completado exitosamente
