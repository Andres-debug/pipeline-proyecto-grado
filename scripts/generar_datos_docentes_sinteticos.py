"""
Script para generar datos sintéticos de movilidad de docentes internacionales
Compatible con el esquema del archivo "Movilidad de docentes del exterior hacia Colombia"

Autor: Pipeline Proyecto de Grado
Fecha: 2025-11-05
"""

import pandas as pd
import numpy as np
from pathlib import Path
import random
from datetime import datetime

# Configuración de reproducibilidad
np.random.seed(42)
random.seed(42)

# Rutas
BASE_DIR = Path(__file__).parent.parent
DATA_RAW_DIR = BASE_DIR / 'data' / 'raw'

# ============================================================================
# DATOS BASE PARA GENERACIÓN SINTÉTICA - DOCENTES
# ============================================================================

# Países (distribución ligeramente diferente para docentes)
PAISES = {
    'ESPAÑA': 0.25,
    'MÉXICO': 0.20,
    'ARGENTINA': 0.15,
    'BRASIL': 0.12,
    'CHILE': 0.10,
    'ESTADOS UNIDOS DE AMÉRICA': 0.08,
    'FRANCIA': 0.04,
    'ITALIA': 0.03,
    'ALEMANIA': 0.02,
    'REINO UNIDO': 0.01
}

# Instituciones extranjeras por país
INSTITUCIONES = {
    'ESPAÑA': ['Universidad de Barcelona', 'Universidad Complutense de Madrid', 'UAM', 'Universidad de Valencia', 'Universidad de Sevilla'],
    'MÉXICO': ['UNAM', 'Tec de Monterrey', 'Universidad de Guadalajara', 'IPN', 'UAM'],
    'ARGENTINA': ['Universidad de Buenos Aires', 'Universidad Nacional de Córdoba', 'UNLP', 'Universidad de Rosario'],
    'BRASIL': ['USP', 'UNICAMP', 'UFRJ', 'UnB', 'UFMG'],
    'CHILE': ['Universidad de Chile', 'PUC Chile', 'Universidad de Concepción', 'USACH'],
    'ESTADOS UNIDOS DE AMÉRICA': ['MIT', 'Harvard', 'Stanford', 'UC Berkeley', 'Columbia', 'Yale'],
    'FRANCIA': ['Sorbonne', 'Sciences Po', 'École Polytechnique', 'Université Paris'],
    'ITALIA': ['Università di Bologna', 'La Sapienza', 'Politecnico di Milano', 'Università di Padova'],
    'ALEMANIA': ['LMU München', 'Heidelberg', 'TU München', 'Humboldt-Universität'],
    'REINO UNIDO': ['Oxford', 'Cambridge', 'Imperial College', 'UCL']
}

# Tipos de movilidad para docentes
TIPOS_MOVILIDAD_DOCENTES = {
    'Docencia': 0.40,
    'Investigación': 0.30,
    'Capacitación': 0.15,
    'Conferencia': 0.10,
    'Asesoría académica': 0.05
}

# Duraciones según tipo de movilidad (días)
DURACIONES = {
    'Docencia': (15, 60),
    'Investigación': (30, 90),
    'Capacitación': (5, 21),
    'Conferencia': (3, 7),
    'Asesoría académica': (7, 30)
}

# Universidades colombianas
UNIVERSIDADES = ['Universidad de Antioquia', 'IUSH', 'UNAC', 'Universidad Nacional']

# ============================================================================
# FUNCIONES DE GENERACIÓN
# ============================================================================

def generar_nombre_docente():
    """Genera un nombre ficticio de docente"""
    nombres = ['John', 'María', 'Carlos', 'Ana', 'Michael', 'Laura', 'David', 'Sofia', 
               'Robert', 'Valentina', 'José', 'Emma', 'Luis', 'Isabella', 'Jorge', 'Elena']
    apellidos = ['Smith', 'García', 'Rodríguez', 'Martínez', 'López', 'González', 'Pérez', 
                 'Johnson', 'Brown', 'Sánchez', 'Silva', 'Costa', 'Fernández', 'Müller']
    
    primer_nombre = random.choice(nombres)
    segundo_nombre = random.choice(nombres) if random.random() > 0.5 else ''
    primer_apellido = random.choice(apellidos)
    segundo_apellido = random.choice(apellidos)
    
    return primer_nombre, segundo_nombre, primer_apellido, segundo_apellido

def generar_documento_extranjero():
    """Genera un número de documento extranjero"""
    tipos = ['PS', 'PA', 'CE', 'DNI']
    tipo = random.choice(tipos)
    
    if tipo == 'PS':
        numero = f"{random.choice(['X', 'Y', 'Z', 'A', 'B', 'C'])}{random.randint(1000000, 99999999)}"
    elif tipo == 'PA':
        numero = f"{random.choice(['PA', 'PB', 'PC'])}{random.randint(100000, 9999999)}"
    elif tipo == 'DNI':
        numero = str(random.randint(10000000, 99999999))
    else:
        numero = str(random.randint(1000000, 99999999))
    
    return tipo, numero

def seleccionar_pais():
    """Selecciona un país basado en probabilidades"""
    return np.random.choice(list(PAISES.keys()), p=list(PAISES.values()))

def seleccionar_institucion(pais):
    """Selecciona una institución del país"""
    return random.choice(INSTITUCIONES.get(pais, ['Universidad Internacional']))

def seleccionar_tipo_movilidad():
    """Selecciona tipo de movilidad basado en probabilidades"""
    return np.random.choice(
        list(TIPOS_MOVILIDAD_DOCENTES.keys()), 
        p=list(TIPOS_MOVILIDAD_DOCENTES.values())
    )

def calcular_duracion(tipo_movilidad):
    """Calcula duración en días según tipo de movilidad"""
    min_dias, max_dias = DURACIONES.get(tipo_movilidad, (7, 30))
    return random.randint(min_dias, max_dias)

def calcular_financiacion(num_dias, pais):
    """Calcula financiación basada en duración y país"""
    # Costo base por día para docentes (generalmente mayor que estudiantes)
    costos_base = {
        'ESPAÑA': 200000,
        'MÉXICO': 180000,
        'ARGENTINA': 150000,
        'BRASIL': 160000,
        'CHILE': 170000,
        'ESTADOS UNIDOS DE AMÉRICA': 300000,
        'FRANCIA': 220000,
        'ITALIA': 210000,
        'ALEMANIA': 230000,
        'REINO UNIDO': 280000
    }
    
    costo_dia = costos_base.get(pais, 180000)
    
    # Agregar variación aleatoria (±25%)
    variacion = random.uniform(0.75, 1.25)
    
    # Financiación (para docentes, mayor proporción nacional)
    financiacion_nacional = int(costo_dia * num_dias * variacion * random.uniform(0.5, 0.8))
    financiacion_internacional = int(costo_dia * num_dias * variacion * random.uniform(0.2, 0.5))
    
    return financiacion_nacional, financiacion_internacional

def obtener_codigo_pais(pais):
    """Obtiene código ISO del país"""
    codigos = {
        'ESPAÑA': 724,
        'MÉXICO': 484,
        'ARGENTINA': 32,
        'BRASIL': 76,
        'CHILE': 152,
        'ESTADOS UNIDOS DE AMÉRICA': 840,
        'FRANCIA': 250,
        'ITALIA': 380,
        'ALEMANIA': 276,
        'REINO UNIDO': 826
    }
    return codigos.get(pais, 999)

# ============================================================================
# GENERACIÓN DEL DATASET DOCENTES
# ============================================================================

def generar_dataset_docentes_sintetico(num_registros=200, años=[2020, 2021, 2022, 2023, 2024, 2025]):
    """
    Genera un dataset sintético de movilidad de docentes
    
    Args:
        num_registros: Número total de registros a generar
        años: Lista de años para los que generar datos
    
    Returns:
        DataFrame con datos sintéticos
    """
    
    print("="*80)
    print("GENERANDO DATOS SINTÉTICOS DE MOVILIDAD DE DOCENTES")
    print("="*80)
    print(f"\nParámetros:")
    print(f"  - Registros a generar: {num_registros:,}")
    print(f"  - Años: {años}")
    print(f"  - Países: {len(PAISES)}")
    print(f"\nGenerando datos...")
    
    registros = []
    
    for i in range(num_registros):
        # Información temporal
        año = random.choice(años)
        semestre = random.choice([1, 2])
        
        # Información personal
        tipo_doc, num_doc = generar_documento_extranjero()
        p_nombre, s_nombre, p_apellido, s_apellido = generar_nombre_docente()
        
        # Información de movilidad
        pais = seleccionar_pais()
        institucion = seleccionar_institucion(pais)
        tipo_movilidad = seleccionar_tipo_movilidad()
        num_dias = calcular_duracion(tipo_movilidad)
        
        # Universidad colombiana receptora
        universidad = random.choice(UNIVERSIDADES)
        
        # Información financiera
        fin_nacional, fin_internacional = calcular_financiacion(num_dias, pais)
        
        # Crear registro (schema compatible con archivo de docentes)
        registro = {
            'AÑO': año,
            'SEMESTRE': semestre,
            'ID_TIPO_DOCUMENTO': tipo_doc,
            'NUM_DOCUMENTO': num_doc,
            'PRIMER_NOMBRE': p_nombre,
            'SEGUNDO_NOMBRE': s_nombre,
            'PRIMER_APELLIDO': p_apellido,
            'SEGUNDO_APELLIDO': s_apellido,
            'PAIS_EXTRANJERO': pais,
            'ID_PAIS_EXTRANJERO': obtener_codigo_pais(pais),
            'INSTITUCION_EXTRANJERA': institucion,
            'UNIVERSIDAD': universidad,  # Universidad colombiana
            'TIPO_MOV_DOC_EXTRANJ': tipo_movilidad,
            'ID_TIPO_MOV_DOC_EXTRANJ': list(TIPOS_MOVILIDAD_DOCENTES.keys()).index(tipo_movilidad) + 1,
            'NUM_DIAS_MOVILIDAD': num_dias,
            'MOVILIDAD_POR_CONVENIO': random.choice(['S', 'N']),
            'CODIGO_CONVENIO': f"CONV-DOC-{random.randint(1000, 9999)}" if random.random() > 0.6 else '',
            'VALOR_FINANCIACION_NACIONAL': fin_nacional,
            'VALOR_FINANCIACION_INTERNAC': fin_internacional,
            'PAIS_FINANCIADOR': pais,
            'ID_PAIS_FINANCIADOR': obtener_codigo_pais(pais)
        }
        
        registros.append(registro)
        
        # Mostrar progreso
        if (i + 1) % 50 == 0:
            print(f"  Generados: {i + 1:,}/{num_registros:,} ({(i+1)/num_registros*100:.1f}%)")
    
    # Crear DataFrame
    df = pd.DataFrame(registros)
    
    print(f"\n✓ Generación completada: {len(df):,} registros")
    
    return df

def generar_estadisticas_docentes(df):
    """Genera estadísticas del dataset sintético de docentes"""
    print("\n" + "="*80)
    print("ESTADÍSTICAS DEL DATASET SINTÉTICO - DOCENTES")
    print("="*80)
    
    print(f"\nTotal de registros: {len(df):,}")
    
    print(f"\n📅 Distribución temporal:")
    print(df.groupby(['AÑO', 'SEMESTRE']).size().to_frame('Registros'))
    
    print(f"\n🌍 Top países:")
    print(df['PAIS_EXTRANJERO'].value_counts())
    
    print(f"\n🎓 Tipos de movilidad:")
    print(df['TIPO_MOV_DOC_EXTRANJ'].value_counts())
    
    print(f"\n🏛️ Universidades receptoras:")
    print(df['UNIVERSIDAD'].value_counts())
    
    print(f"\n📊 Estadísticas de duración:")
    print(df['NUM_DIAS_MOVILIDAD'].describe())
    
    print(f"\n💰 Estadísticas financieras:")
    df['FINANCIACION_TOTAL'] = df['VALOR_FINANCIACION_NACIONAL'] + df['VALOR_FINANCIACION_INTERNAC']
    print(df['FINANCIACION_TOTAL'].describe())

# ============================================================================
# SCRIPT PRINCIPAL
# ============================================================================

if __name__ == "__main__":
    print("\n" + "="*80)
    print("GENERADOR DE DATOS SINTÉTICOS - MOVILIDAD DE DOCENTES")
    print("="*80)
    print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Parámetros
    NUM_REGISTROS = 200  # Menos registros que estudiantes (más realista)
    AÑOS = [2020, 2021, 2022, 2023, 2024, 2025]
    
    # Generar datos
    df_sintetico = generar_dataset_docentes_sintetico(NUM_REGISTROS, AÑOS)
    
    # Mostrar estadísticas
    generar_estadisticas_docentes(df_sintetico)
    
    # Guardar archivo CSV
    output_csv = DATA_RAW_DIR / 'docentes_exterior_sintetico.csv'
    df_sintetico.to_csv(output_csv, index=False)
    print(f"\n✓ Datos CSV guardados en: {output_csv}")
    
    # Guardar también como Excel (compatible con el esquema original)
    output_excel = DATA_RAW_DIR / 'docentes_exterior_sintetico.xlsx'
    df_sintetico.to_excel(output_excel, index=False, sheet_name='Datos')
    print(f"✓ Datos Excel guardados en: {output_excel}")
    
    print("\n" + "="*80)
    print("PROCESO COMPLETADO EXITOSAMENTE")
    print("="*80)
    print("\nArchivos generados:")
    print(f"  1. {output_csv} - Formato CSV")
    print(f"  2. {output_excel} - Formato Excel")
    print("\nPróximos pasos:")
    print("  - Ejecutar notebook 02 para consolidar todos los datos")
    print("  - El sistema cargará automáticamente todos los archivos disponibles")
