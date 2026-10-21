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

ARCHIVO_DATOS = "expedientes.txt"
SEPARADOR = "|"

TIPOS_TRAMITE_VALIDOS = [
    "certificado", "permiso", "reclamo", "comunicacion",
    "tesoreria", "informe de salud", "apoyo"
]

def cargar_expedientes():
    """
    Lee el archivo de texto y reconstruye la lista de expedientes.
    Cada expediente se representa como un diccionario (registro),
    para evitar el riesgo de desalineación de los arreglos paralelos.
    Si el archivo no existe todavía, devuelve una lista vacía.
    """
    expedientes = []

    if not os.path.exists(ARCHIVO_DATOS):
        return expedientes

    archivo = open(ARCHIVO_DATOS, "r", encoding="utf-8")
    for linea in archivo:
        linea = linea.strip()
        if linea == "":
            continue
        campos = linea.split(SEPARADOR)
        if len(campos) != 9:
            continue

        expediente = {
            "numero": int(campos[0]),
            "nombre": campos[1],
            "dni": campos[2],
            "tipo_tramite": campos[3],
            "fecha": campos[4],
            "celular": campos[5],
            "correo": campos[6],
            "descripcion": campos[7],
            "estado": campos[8]
        }
        expedientes.append(expediente)
    archivo.close()

    return expedientes

def guardar_expedientes(expedientes):
    """
    Escribe TODA la lista de expedientes en el archivo de texto,
    un expediente por línea, con los campos unidos por SEPARADOR.
    """
    archivo = open(ARCHIVO_DATOS, "w", encoding="utf-8")
    for exp in expedientes:
        linea = SEPARADOR.join([
            str(exp["numero"]),
            exp["nombre"],
            exp["dni"],
            exp["tipo_tramite"],
            exp["fecha"],
            exp["celular"],
            exp["correo"],
            exp["descripcion"],
            exp["estado"]
        ])
        archivo.write(linea + "\n")
    archivo.close()

def validar_texto_no_vacio(texto):
    """Devuelve True si el texto tiene contenido real (no solo espacios)."""
    return texto.strip() != ""


def validar_dni(dni):
    """
    Un DNI peruano válido tiene 8 dígitos numéricos.
    Según la entrevista, el DNI solo es obligatorio para certificados,
    por eso esta función se usa condicionalmente, no siempre.
    """
    return dni.isdigit() and len(dni) == 8


def validar_celular(celular):
    """Un celular válido en Perú tiene 9 dígitos numéricos."""
    return celular.isdigit() and len(celular) == 9

def obtener_siguiente_numero(expedientes):
    """
    Calcula el siguiente número de expediente correlativo,
    igual que en el cuaderno físico de la secretaria.
    """
    if len(expedientes) == 0:
        return 1
    numeros = [exp["numero"] for exp in expedientes]
    return max(numeros) + 1



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