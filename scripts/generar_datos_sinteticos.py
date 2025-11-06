"""
Script para generar datos sintéticos de movilidad académica internacional
Basado en los patrones de datos reales del IUSH

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
# DATOS BASE PARA GENERACIÓN SINTÉTICA
# ============================================================================

# Países con sus probabilidades (basado en datos reales)
PAISES = {
    'MÉXICO': 0.30,
    'ESPAÑA': 0.20,
    'BRASIL': 0.15,
    'ITALIA': 0.12,
    'GRECIA': 0.10,
    'ESTADOS UNIDOS DE AMÉRICA': 0.05,
    'TURQUÍA': 0.03,
    'RUMANÍA': 0.02,
    'VENEZUELA': 0.02,
    'FRANCIA': 0.01
}

# Instituciones extranjeras por país
INSTITUCIONES = {
    'MÉXICO': ['Econométrica', 'UNAM', 'Tec de Monterrey', 'Universidad Iberoamericana', 'ITESM'],
    'ESPAÑA': ['Innética', 'Universidad de Barcelona', 'UAM', 'Universidad Complutense', 'IE Business School'],
    'BRASIL': ['Cooperbom', 'USP', 'UNICAMP', 'PUC-Rio', 'FGV'],
    'ITALIA': ['RAS', 'Università di Bologna', 'Politecnico di Milano', 'La Sapienza', 'Bocconi'],
    'GRECIA': ['Action', 'Universidad de Atenas', 'Aristotle University', 'Technical University of Athens'],
    'ESTADOS UNIDOS DE AMÉRICA': ['MIT', 'Harvard', 'Stanford', 'Berkeley', 'Columbia'],
    'TURQUÍA': ['Innética', 'Boğaziçi University', 'Middle East Technical University', 'Istanbul University'],
    'RUMANÍA': ['Innética', 'Universitatea din București', 'Universitatea Babeș-Bolyai'],
    'VENEZUELA': ['Cooperbom', 'UCV', 'USB', 'UCAB'],
    'FRANCIA': ['Sorbonne', 'Sciences Po', 'HEC Paris', 'École Polytechnique']
}

# Tipos de movilidad
TIPOS_MOVILIDAD = {
    'Curso corto': 0.60,
    'Pasantía': 0.20,
    'Intercambio académico': 0.10,
    'Investigación': 0.05,
    'Conferencia': 0.03,
    'Workshop': 0.02
}

# Duraciones según tipo de movilidad (días)
DURACIONES = {
    'Curso corto': (5, 15),
    'Pasantía': (30, 90),
    'Intercambio académico': (90, 180),
    'Investigación': (60, 120),
    'Conferencia': (3, 7),
    'Workshop': (3, 10)
}

# Universidades colombianas
UNIVERSIDADES = ['IUSH', 'Universidad de Antioquia', 'UNAC']

# Fuentes de financiación
FUENTES_FINANCIACION = [
    'Organismo Multilateral',
    'Recursos Propios',
    'Beca Institucional',
    'Convenio Bilateral',
    'Gobierno Colombiano',
    'ONG Internacional'
]

# ============================================================================
# FUNCIONES DE GENERACIÓN
# ============================================================================

def generar_nombre_persona():
    """Genera un nombre ficticio"""
    nombres = ['Juan', 'María', 'Carlos', 'Ana', 'Luis', 'Laura', 'Pedro', 'Sofia', 
               'Miguel', 'Valentina', 'David', 'Camila', 'Daniel', 'Isabella', 'Jorge']
    apellidos = ['García', 'Rodríguez', 'Martínez', 'López', 'González', 'Pérez', 
                 'Sánchez', 'Ramírez', 'Torres', 'Flores', 'Rivera', 'Gómez']
    
    primer_nombre = random.choice(nombres)
    segundo_nombre = random.choice(nombres) if random.random() > 0.3 else ''
    primer_apellido = random.choice(apellidos)
    segundo_apellido = random.choice(apellidos)
    
    return primer_nombre, segundo_nombre, primer_apellido, segundo_apellido

def generar_documento():
    """Genera un número de documento ficticio"""
    tipos = ['PS', 'CC', 'CE', 'PA']
    tipo = random.choice(tipos)
    
    if tipo == 'PS':
        numero = f"{random.choice(['G', 'N', 'Y', 'F', 'A', 'U'])}{random.randint(10000000, 99999999)}"
    elif tipo == 'PA':
        numero = f"{random.choice(['PA', 'AT', 'BA', 'YC', 'YB'])}{random.randint(100000, 9999999)}"
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
    return np.random.choice(list(TIPOS_MOVILIDAD.keys()), p=list(TIPOS_MOVILIDAD.values()))

def calcular_duracion(tipo_movilidad):
    """Calcula duración en días según tipo de movilidad"""
    min_dias, max_dias = DURACIONES.get(tipo_movilidad, (7, 30))
    return random.randint(min_dias, max_dias)

def calcular_financiacion(num_dias, pais):
    """Calcula financiación basada en duración y país"""
    # Costo base por día (varía según destino)
    costos_base = {
        'MÉXICO': 150000,
        'ESPAÑA': 180000,
        'BRASIL': 140000,
        'ITALIA': 190000,
        'GRECIA': 160000,
        'ESTADOS UNIDOS DE AMÉRICA': 250000,
        'TURQUÍA': 130000,
        'RUMANÍA': 120000,
        'VENEZUELA': 100000,
        'FRANCIA': 200000
    }
    
    costo_dia = costos_base.get(pais, 150000)
    
    # Agregar variación aleatoria (±20%)
    variacion = random.uniform(0.8, 1.2)
    
    # Financiación total
    financiacion_nacional = int(costo_dia * num_dias * variacion * random.uniform(0.3, 0.7))
    financiacion_internacional = int(costo_dia * num_dias * variacion * random.uniform(0.3, 0.7))
    
    return financiacion_nacional, financiacion_internacional

def obtener_codigo_pais(pais):
    """Obtiene código ISO del país"""
    codigos = {
        'MÉXICO': 484,
        'ESPAÑA': 724,
        'BRASIL': 76,
        'ITALIA': 380,
        'GRECIA': 300,
        'ESTADOS UNIDOS DE AMÉRICA': 840,
        'TURQUÍA': 792,
        'RUMANÍA': 642,
        'VENEZUELA': 862,
        'FRANCIA': 250
    }
    return codigos.get(pais, 999)

# ============================================================================
# GENERACIÓN DEL DATASET
# ============================================================================

def generar_dataset_sintetico(num_registros=500, años=[2020, 2021, 2022, 2023, 2024, 2025]):
    """
    Genera un dataset sintético de movilidad académica
    
    Args:
        num_registros: Número total de registros a generar
        años: Lista de años para los que generar datos
    
    Returns:
        DataFrame con datos sintéticos
    """
    
    print("="*80)
    print("GENERANDO DATOS SINTÉTICOS DE MOVILIDAD ACADÉMICA")
    print("="*80)
    print(f"\nParámetros:")
    print(f"  - Registros a generar: {num_registros:,}")
    print(f"  - Años: {años}")
    print(f"  - Universidades: {len(UNIVERSIDADES)}")
    print(f"  - Países: {len(PAISES)}")
    print(f"\nGenerando datos...")
    
    registros = []
    
    for i in range(num_registros):
        # Información temporal
        año = random.choice(años)
        semestre = random.choice([1, 2])
        
        # Información personal
        tipo_doc, num_doc = generar_documento()
        p_nombre, s_nombre, p_apellido, s_apellido = generar_nombre_persona()
        
        # Información de movilidad
        pais = seleccionar_pais()
        institucion = seleccionar_institucion(pais)
        tipo_movilidad = seleccionar_tipo_movilidad()
        num_dias = calcular_duracion(tipo_movilidad)
        
        # Información financiera
        fin_nacional, fin_internacional = calcular_financiacion(num_dias, pais)
        
        # País financiador (generalmente el país de destino o Colombia)
        pais_financiador = pais if random.random() > 0.3 else 'COLOMBIA'
        if pais_financiador == 'COLOMBIA':
            pais_financiador = pais  # Para simplificar, usamos el país de destino
        
        # Crear registro
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
            'TIPO_MOV_EST_EXTRANJ': tipo_movilidad,
            'ID_TIPO_MOV_EST_EXTRANJ': list(TIPOS_MOVILIDAD.keys()).index(tipo_movilidad) + 1,
            'NUM_DIAS_MOVILIDAD': num_dias,
            'MOVILIDAD_POR_CONVENIO': random.choice(['S', 'N']),
            'CODIGO_CONVENIO': f"CONV-{random.randint(1000, 9999)}" if random.random() > 0.5 else '',
            'FUENTE_NACIONAL_INVESTIG': random.choice(FUENTES_FINANCIACION),
            'ID_FUENTE_NACIONAL_INVESTIG': random.randint(1, 10),
            'VALOR_FINANCIACION_NACIONAL': fin_nacional,
            'FUENTE_INTERNACIONAL': random.choice(FUENTES_FINANCIACION),
            'ID_FUENTE_INTERNACIONAL': random.randint(1, 10),
            'PAIS_FINANCIADOR': pais_financiador,
            'ID_PAIS_FINANCIADOR': obtener_codigo_pais(pais_financiador),
            'VALOR_FINANCIACION_INTERNAC': fin_internacional
        }
        
        registros.append(registro)
        
        # Mostrar progreso
        if (i + 1) % 100 == 0:
            print(f"  Generados: {i + 1:,}/{num_registros:,} ({(i+1)/num_registros*100:.1f}%)")
    
    # Crear DataFrame
    df = pd.DataFrame(registros)
    
    print(f"\n✓ Generación completada: {len(df):,} registros")
    
    return df

def generar_estadisticas(df):
    """Genera estadísticas del dataset sintético"""
    print("\n" + "="*80)
    print("ESTADÍSTICAS DEL DATASET SINTÉTICO")
    print("="*80)
    
    print(f"\nTotal de registros: {len(df):,}")
    
    print(f"\n📅 Distribución temporal:")
    print(df.groupby(['AÑO', 'SEMESTRE']).size().to_frame('Registros'))
    
    print(f"\n🌍 Top 10 países:")
    print(df['PAIS_EXTRANJERO'].value_counts().head(10))
    
    print(f"\n🎓 Tipos de movilidad:")
    print(df['TIPO_MOV_EST_EXTRANJ'].value_counts())
    
    print(f"\n📊 Estadísticas de duración:")
    print(df['NUM_DIAS_MOVILIDAD'].describe())
    
    print(f"\n💰 Estadísticas financieras:")
    df['FINANCIACION_TOTAL'] = df['VALOR_FINANCIACION_NACIONAL'] + df['VALOR_FINANCIACION_INTERNAC']
    print(df['FINANCIACION_TOTAL'].describe())
    
    print(f"\n🏛️ Top instituciones:")
    print(df['INSTITUCION_EXTRANJERA'].value_counts().head(10))

# ============================================================================
# SCRIPT PRINCIPAL
# ============================================================================

if __name__ == "__main__":
    print("\n" + "="*80)
    print("GENERADOR DE DATOS SINTÉTICOS - MOVILIDAD ACADÉMICA INTERNACIONAL")
    print("="*80)
    print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Parámetros
    NUM_REGISTROS = 500  # Cambiar según necesidad
    AÑOS = [2020, 2021, 2022, 2023, 2024, 2025]
    
    # Generar datos
    df_sintetico = generar_dataset_sintetico(NUM_REGISTROS, AÑOS)
    
    # Mostrar estadísticas
    generar_estadisticas(df_sintetico)
    
    # Guardar archivo
    output_file = DATA_RAW_DIR / 'iush_sintetico.csv'
    df_sintetico.to_csv(output_file, index=False)
    print(f"\n✓ Datos guardados en: {output_file}")
    
    # También combinar con datos reales si existen
    try:
        df_real = pd.read_csv(DATA_RAW_DIR / 'iush.csv')
        # Limpiar filas vacías
        df_real = df_real.dropna(subset=['AÑO', 'SEMESTRE'])
        
        print(f"\n📁 Datos reales encontrados: {len(df_real):,} registros")
        
        # Combinar
        df_combinado = pd.concat([df_real, df_sintetico], ignore_index=True)
        
        output_combinado = DATA_RAW_DIR / 'iush_completo.csv'
        df_combinado.to_csv(output_combinado, index=False)
        
        print(f"✓ Dataset combinado guardado: {output_combinado}")
        print(f"  Total registros: {len(df_combinado):,}")
        print(f"    - Reales: {len(df_real):,}")
        print(f"    - Sintéticos: {len(df_sintetico):,}")
        
    except FileNotFoundError:
        print(f"\n⚠ No se encontró archivo de datos reales, solo se guardó dataset sintético")
    
    print("\n" + "="*80)
    print("PROCESO COMPLETADO EXITOSAMENTE")
    print("="*80)
    print("\nArchivos generados:")
    print(f"  1. {DATA_RAW_DIR / 'iush_sintetico.csv'} - Solo datos sintéticos")
    if (DATA_RAW_DIR / 'iush_completo.csv').exists():
        print(f"  2. {DATA_RAW_DIR / 'iush_completo.csv'} - Datos reales + sintéticos")
    print("\nPróximos pasos:")
    print("  - Ejecutar notebook 01 para cargar y explorar los datos")
    print("  - Ejecutar notebook 02 para limpiar y estandarizar")
    print("  - Continuar con el pipeline completo")
