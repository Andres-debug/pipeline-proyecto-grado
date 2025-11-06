"""
Script maestro para generar todos los datos sintéticos del proyecto
Ejecuta generadores de estudiantes y docentes

Autor: Pipeline Proyecto de Grado
Fecha: 2025-11-05
"""

import subprocess
import sys
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).parent.parent

print("\n" + "="*80)
print("GENERADOR MAESTRO DE DATOS SINTÉTICOS")
print("Proyecto: Arquitectura de BI - Turismo Académico Medellín")
print("="*80)
print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

# ============================================================================
# EJECUTAR GENERADORES
# ============================================================================

scripts = [
    {
        'nombre': 'Estudiantes Internacionales',
        'archivo': 'generar_datos_sinteticos.py',
        'descripcion': 'Genera datos de movilidad estudiantil'
    },
    {
        'nombre': 'Docentes Internacionales',
        'archivo': 'generar_datos_docentes_sinteticos.py',
        'descripcion': 'Genera datos de movilidad de docentes'
    }
]

resultados = []

for i, script in enumerate(scripts, 1):
    print(f"\n{'='*80}")
    print(f"EJECUTANDO {i}/{len(scripts)}: {script['nombre']}")
    print(f"{'='*80}")
    print(f"Descripción: {script['descripcion']}\n")
    
    script_path = Path(__file__).parent / script['archivo']
    
    try:
        # Ejecutar script
        result = subprocess.run(
            [sys.executable, str(script_path)],
            capture_output=True,
            text=True,
            cwd=BASE_DIR
        )
        
        # Mostrar output
        print(result.stdout)
        
        if result.returncode == 0:
            resultados.append({
                'script': script['nombre'],
                'estado': '✓ ÉXITO',
                'codigo': result.returncode
            })
            print(f"\n✅ {script['nombre']} - Completado exitosamente")
        else:
            resultados.append({
                'script': script['nombre'],
                'estado': '✗ ERROR',
                'codigo': result.returncode
            })
            print(f"\n❌ {script['nombre']} - Error en ejecución")
            if result.stderr:
                print(f"Error: {result.stderr}")
    
    except Exception as e:
        resultados.append({
            'script': script['nombre'],
            'estado': '✗ EXCEPCIÓN',
            'codigo': -1
        })
        print(f"\n❌ {script['nombre']} - Excepción: {str(e)}")

# ============================================================================
# RESUMEN FINAL
# ============================================================================

print("\n" + "="*80)
print("RESUMEN DE GENERACIÓN")
print("="*80)

for resultado in resultados:
    print(f"\n{resultado['estado']} {resultado['script']}")
    if resultado['codigo'] != 0:
        print(f"   Código de salida: {resultado['codigo']}")

# Contar éxitos
exitos = sum(1 for r in resultados if r['codigo'] == 0)
total = len(resultados)

print("\n" + "="*80)
if exitos == total:
    print("🎉 TODOS LOS DATOS GENERADOS EXITOSAMENTE")
    print("="*80)
    print(f"\n✓ {exitos}/{total} generadores ejecutados correctamente")
    print("\nArchivos generados en data/raw/:")
    print("  - iush_sintetico.csv")
    print("  - iush_completo.csv (si había datos reales)")
    print("  - docentes_exterior_sintetico.csv")
    print("  - docentes_exterior_sintetico.xlsx")
    print("\nPróximos pasos:")
    print("  1. Ejecutar notebook 02 para consolidar todos los datos")
    print("  2. Continuar con el pipeline de análisis (notebooks 03-05)")
    print("  3. Los datos sintéticos se integrarán automáticamente")
else:
    print("⚠️ GENERACIÓN COMPLETADA CON ERRORES")
    print("="*80)
    print(f"\n✓ {exitos}/{total} generadores ejecutados correctamente")
    print(f"✗ {total - exitos}/{total} generadores con errores")
    print("\nRevisar logs arriba para detalles de los errores")

print("\n" + "="*80)
print(f"Proceso finalizado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("="*80 + "\n")

# Código de salida
sys.exit(0 if exitos == total else 1)
