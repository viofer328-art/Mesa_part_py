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

<<<<<<< HEAD
ARCHIVO_DATOS = "expedientes.txt"
SEPARADOR = "|"
=======
# ------------------------------------------------------------
# CONSTANTES GLOBALES
# ------------------------------------------------------------
ARCHIVO_DATOS = "expedientes.txt"
SEPARADOR = "|"   # separador de campos dentro del archivo de texto
>>>>>>> b846383500f034e2a8f1de4f6bb94348eeea85f5

TIPOS_TRAMITE_VALIDOS = [
    "certificado", "permiso", "reclamo", "comunicacion",
    "tesoreria", "informe de salud", "apoyo"
]

<<<<<<< HEAD
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


def registrar_expediente(expedientes):
    """
    Pide los datos de un nuevo trámite, los valida y agrega
    el nuevo expediente a la lista (arreglo de registros).
    """
    print("\n--- REGISTRAR NUEVO EXPEDIENTE ---")

    nombre = input("Nombre completo del solicitante: ").strip()
    while not validar_texto_no_vacio(nombre):
        print("El nombre no puede estar vacío.")
        nombre = input("Nombre completo del solicitante: ").strip()

    print("Tipos de trámite disponibles:", ", ".join(TIPOS_TRAMITE_VALIDOS))
    tipo_tramite = input("Tipo de trámite: ").strip().lower()
    while tipo_tramite not in TIPOS_TRAMITE_VALIDOS:
        print("Tipo de trámite no reconocido. Intente nuevamente.")
        tipo_tramite = input("Tipo de trámite: ").strip().lower()

    if tipo_tramite == "certificado":
        dni = input("DNI del solicitante (8 dígitos, requerido para certificados): ").strip()

        while not validar_dni(dni):
            print("DNI inválido. Debe tener 8 dígitos numéricos.")
            dni = input("DNI del solicitante: ").strip()
    else:
        dni = input("DNI del solicitante (opcional, Enter para omitir): ").strip()
        if dni != "" and not validar_dni(dni):
            print("Aviso: el DNI ingresado no tiene el formato correcto, se guardará igual.")

    fecha = input("Fecha de ingreso (DD/MM/AAAA): ").strip()
    while not validar_texto_no_vacio(fecha):
        print("La fecha no puede estar vacía.")
        fecha = input("Fecha de ingreso (DD/MM/AAAA): ").strip()

    celular = input("Número de celular (9 dígitos): ").strip()
    while not validar_celular(celular):
        print("Celular inválido. Debe tener 9 dígitos numéricos.")
        celular = input("Número de celular: ").strip()

    correo = input("Correo electrónico (opcional): ").strip()

    descripcion = input("Descripción del pedido/asunto: ").strip()
    while not validar_texto_no_vacio(descripcion):
        print("La descripción no puede estar vacía.")
        descripcion = input("Descripción del pedido/asunto: ").strip()

    numero = obtener_siguiente_numero(expedientes)

    nuevo_expediente = {
        "numero": numero,
        "nombre": nombre,
        "dni": dni,
        "tipo_tramite": tipo_tramite,
        "fecha": fecha,
        "celular": celular,
        "correo": correo,
        "descripcion": descripcion,
        "estado": "registrado"
    }

    expedientes.append(nuevo_expediente)
    guardar_expedientes(expedientes)

    print(f"\nExpediente registrado con éxito. N° de expediente: {numero}")
=======
>>>>>>> b846383500f034e2a8f1de4f6bb94348eeea85f5

def mostrar_expediente(exp):
    """Imprime en pantalla los datos de un solo expediente."""
    print("-" * 50)
    print(f"N° Expediente : {exp['numero']}")
    print(f"Solicitante   : {exp['nombre']}")
    print(f"DNI           : {exp['dni'] if exp['dni'] else '(no registrado)'}")
    print(f"Tipo trámite  : {exp['tipo_tramite']}")
    print(f"Fecha ingreso : {exp['fecha']}")
    print(f"Celular       : {exp['celular']}")
    print(f"Correo        : {exp['correo'] if exp['correo'] else '(no registrado)'}")
    print(f"Descripción   : {exp['descripcion']}")
    print(f"Estado        : {exp['estado']}")
    print("-" * 50)

def buscar_por_numero(expedientes, numero):
    """
    Búsqueda lineal por número de expediente (Tema 3: búsqueda en arreglos).
    Devuelve el expediente encontrado o None si no existe.
    """
    for exp in expedientes:
        if exp["numero"] == numero:
            return exp
    return None


def buscar_por_nombre(expedientes, texto_buscado):
    """
    Búsqueda lineal por coincidencia parcial de nombre (Tema 4: cadenas).
    Devuelve una lista con todas las coincidencias (puede haber varias
    personas con nombres parecidos).
    """
    resultados = []
    texto_buscado = texto_buscado.lower()
    for exp in expedientes:
        if texto_buscado in exp["nombre"].lower():
            resultados.append(exp)
    return resultados

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