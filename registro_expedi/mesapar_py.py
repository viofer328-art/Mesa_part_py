"""
==================================================================
 SISTEMA DE MESA DE PARTES DIGITAL
 Institución Educativa "Coronel Cortegana" - Celendín
 Curso: Fundamentos de Programación (CIIN1205P)
==================================================================
 Este programa reemplaza el registro manual en cuaderno por un
 sistema digital que permite:
   - Registrar expedientes (con validación de datos)
   - Buscar expedientes (por número y por nombre)
   - Ordenar expedientes (algoritmos de burbuja y selección)
   - Marcar expedientes como entregados
   - Guardar y recuperar todo desde un archivo de texto
     (persistencia de datos - Tema 5)
==================================================================
"""

import os

# ------------------------------------------------------------
# CONSTANTES GLOBALES
# ------------------------------------------------------------
ARCHIVO_DATOS = "expedientes.txt"
SEPARADOR = "|"   # separador de campos dentro del archivo de texto

TIPOS_TRAMITE_VALIDOS = [
    "certificado", "permiso", "reclamo", "comunicacion",
    "tesoreria", "informe de salud", "apoyo"
]



def mostrar_menu():
    print("\n==========================================")
    print(" SISTEMA DE MESA DE PARTES")
    print(" I.E. Coronel Cortegana - Celendín")
    print("==========================================")
    print("1. Registrar nuevo expediente")
    print("2. Buscar expediente por número")
    print("3. Buscar expediente por nombre")
    print("4. Listar todos los expedientes")
    print("5. Ordenar expedientes por fecha (burbuja)")
    print("6. Ordenar expedientes por número (selección)")
    print("7. Marcar expediente como entregado")
    print("8. Salir")
    print("==========================================")