# 🔄 Configuración de Datos: Reales vs Sintéticos

## ✅ Cambio Realizado

He actualizado el **Notebook 02** para que use automáticamente los datos sintéticos generados.

---

## 📁 Archivos que se Cargarán Ahora

### Notebook 02 (ETL y Consolidación)

**Antes:**
```python
ruta_iush = DATA_RAW_DIR / 'iush.csv'  # Solo 27 registros reales
```

**Ahora:**
```python
ruta_iush = DATA_RAW_DIR / 'iush_completo.csv'  # 527 registros (27 reales + 500 sintéticos)
ruta_docentes = DATA_RAW_DIR / 'docentes_exterior_sintetico.csv'  # 200 registros sintéticos
```

**Resultado Total:** 727 registros consolidados

---

## 🎯 Opciones Disponibles (Ya Configuradas en el Notebook)

En la celda de carga del Notebook 02, encontrarás estas opciones comentadas:

### Para Estudiantes:

```python
# Opción A: Usar datos completos (reales + sintéticos) - ✅ ACTIVA POR DEFECTO
ruta_iush = DATA_RAW_DIR / 'iush_completo.csv'

# Opción B: Usar solo sintéticos
# ruta_iush = DATA_RAW_DIR / 'iush_sintetico.csv'

# Opción C: Usar solo reales
# ruta_iush = DATA_RAW_DIR / 'iush.csv'
```

### Para Docentes:

```python
# Opción A: Usar datos sintéticos (CSV) - ✅ ACTIVA POR DEFECTO
ruta_docentes = DATA_RAW_DIR / 'docentes_exterior_sintetico.csv'

# Opción B: Usar datos sintéticos (Excel)
# ruta_docentes = DATA_RAW_DIR / 'docentes_exterior_sintetico.xlsx'

# Opción C: Usar datos reales originales
# ruta_docentes = DATA_RAW_DIR / '2. Movilidad_de_docentes_del_exterior_hacia_colombia.xlsx'
```

---

## 🚀 Cómo Cambiar Entre Datasets

Si quieres cambiar qué datos usar:

1. **Abre el Notebook 02**
2. **Ve a la celda 9** (la que dice "=== Carga de fuentes con esquema variable ===")
3. **Comenta/descomenta** la línea que quieras usar:

```python
# Ejemplo: Cambiar a solo sintéticos
# ruta_iush = DATA_RAW_DIR / 'iush_completo.csv'    # <- Comentar esta
ruta_iush = DATA_RAW_DIR / 'iush_sintetico.csv'     # <- Descomentar esta
```

---

## 📊 Comparación de Datasets

| Dataset | Estudiantes | Docentes | Total | Uso Recomendado |
|---------|-------------|----------|-------|-----------------|
| **Solo Reales** | 27 | 0 | 27 | Validación inicial |
| **Solo Sintéticos** | 500 | 200 | 700 | Pruebas y desarrollo |
| **Completo (Recomendado)** | 527 | 200 | **727** | **Análisis completo** ✅ |

---

## ✅ ¿Qué Notebooks Están Listos?

### ✅ Notebook 01 - Carga y Exploración
- **Estado:** Funciona con cualquier dataset
- **Acción:** Ninguna, funciona automáticamente

### ✅ Notebook 02 - ETL y Limpieza  
- **Estado:** Actualizado para usar `iush_completo.csv`
- **Acción:** Ninguna, ya está configurado ✅

### ✅ Notebook 03 - Análisis Descriptivo
- **Estado:** Lee `datos_consolidados_limpios.csv` generado por Notebook 02
- **Acción:** Ninguna, funciona automáticamente

### ✅ Notebook 04 - Modelos Predictivos
- **Estado:** Lee datos procesados
- **Acción:** Ninguna, ahora tendrá suficientes datos para ARIMA ✅

### ✅ Notebook 05 - Power BI
- **Estado:** Lee datos procesados
- **Acción:** Ninguna, funciona automáticamente

---

## 🎯 Workflow Completo

```bash
# 1. Activar entorno
.venv\Scripts\Activate.ps1

# 2. (Opcional) Regenerar datos sintéticos si quieres más/diferentes datos
python scripts\generar_todos_datos_sinteticos.py

# 3. Ejecutar notebooks en orden
jupyter notebook

# Luego ejecutar en orden:
# - 01_carga_exploracion_datos.ipynb
# - 02_limpieza_estandarizacion_etl.ipynb  ← Ahora carga 727 registros
# - 03_analisis_descriptivo.ipynb
# - 04_modelos_predictivos.ipynb          ← Ahora tiene suficientes datos
# - 05_integracion_powerbi_exportacion.ipynb
```

---

## 📈 Ventajas de la Configuración Actual

✅ **Dataset robusto:** 727 registros vs 27 originales (aumento del 2,596%)
✅ **Modelos predictivos viables:** ARIMA necesita mínimo 50 registros, ahora tienes 527
✅ **Análisis temporal:** 6 años de datos (2020-2025) vs 1 semestre
✅ **Diversidad geográfica:** 10+ países representados
✅ **Múltiples tipos de movilidad:** 6 tipos para estudiantes + 5 para docentes
✅ **Fácil cambio:** Solo comentar/descomentar líneas para cambiar dataset
✅ **Preserva datos reales:** Los 27 registros reales están incluidos

---

## 🔧 Personalización Avanzada

### Cambiar cantidad de datos sintéticos:

Edita los scripts de generación:

```python
# En scripts/generar_datos_sinteticos.py
NUM_REGISTROS = 1000  # Cambiar de 500 a 1000

# En scripts/generar_datos_docentes_sinteticos.py  
NUM_REGISTROS = 400   # Cambiar de 200 a 400
```

Luego regenera:

```bash
python scripts\generar_todos_datos_sinteticos.py
```

### Cambiar años generados:

```python
# En ambos scripts
AÑOS = [2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025]  # Agregar más años
```

---

## ❓ Preguntas Frecuentes

### ¿Necesito modificar algo más?
**No.** Solo el Notebook 02 fue actualizado. El resto funciona automáticamente.

### ¿Cómo vuelvo a los datos reales?
Edita la celda 9 del Notebook 02 y cambia a `iush.csv`.

### ¿Los datos sintéticos son realistas?
Sí, están basados en distribuciones de los datos reales con lógica de negocio aplicada.

### ¿Puedo mezclar datos?
Sí, `iush_completo.csv` ya mezcla 27 reales + 500 sintéticos.

### ¿Afecta a Power BI?
No, Power BI lee los archivos exportados del Notebook 05, independiente del origen.

---

## 📞 Soporte

Para más información:
- **Documentación completa:** `scripts/README.md`
- **Resumen ejecutivo:** `DATOS_SINTETICOS_RESUMEN.md`
- **Código fuente:** `scripts/generar_datos_sinteticos.py`

---

**Fecha de actualización:** 2025-11-05
**Estado:** ✅ Configurado y listo para usar
