import os
import json
import re
import shutil
from datetime import datetime

# ============================================================
# SISTEMA DE MESA DE PARTES DIGITAL
# Institución Educativa "Coronel Cortegana" - Celendín
# ============================================================

ARCHIVO_DATOS = "expedientes.txt"
ARCHIVO_RESPALDO = "respaldo_expedientes.bin"
ARCHIVO_SECUENCIA = "ultimo_numero.json"
SEPARADOR = "|"

TIPOS_TRAMITE_VALIDOS = [
    "certificado",
    "permiso",
    "reclamo",
    "comunicacion",
    "tesoreria",
    "informe de salud",
    "apoyo"
]

ESTADOS_VALIDOS = [
    "registrado",
    "en proceso",
    "entregado"
]

TOTAL_OPERACIONES = 0

# ============================================================
# VALIDACIONES Y FUNCIONES AUXILIARES
# ============================================================

def validar_texto_no_vacio(texto):
    return texto.strip() != ""


def validar_dni(dni):
    return bool(re.fullmatch(r"[0-9]{8}", dni))


def validar_celular(celular):
    return bool(re.fullmatch(r"[0-9]{9}", celular))


def validar_fecha(fecha):
    if not re.fullmatch(r"[0-9]{2}/[0-9]{2}/[0-9]{4}", fecha):
        return False
    try:
        datetime.strptime(fecha, "%d/%m/%Y")
        return True
    except ValueError:
        return False


def validar_correo(correo):
    if correo == "":
        return True
    # Comprobación básica de formato, sin verificar la existencia del buzón.
    return bool(re.fullmatch(
        r"[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@"
        r"[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?"
        r"(?:\.[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?)+",
        correo
    )) and ".." not in correo


def limpiar_texto(texto):
    """
    Evita que los datos ingresados dañen la estructura
    del archivo de texto.
    """
    return texto.strip().replace(SEPARADOR, " ").replace("\n", " ")


def solicitar_texto(mensaje):
    texto = limpiar_texto(input(mensaje))

    while not validar_texto_no_vacio(texto):
        print("Este campo no puede quedar vacío.")
        texto = limpiar_texto(input(mensaje))

    return texto


def solicitar_dni(obligatorio=True):
    while True:
        dni = input("DNI del solicitante: ").strip()

        if dni == "" and not obligatorio:
            return ""

        if validar_dni(dni):
            return dni

        print("El DNI debe contener exactamente 8 dígitos.")

        if not obligatorio:
            print("También puede presionar Enter para omitirlo.")


def solicitar_celular():
    while True:
        celular = input("Número de celular: ").strip()

        if validar_celular(celular):
            return celular

        print("El celular debe contener exactamente 9 dígitos.")


def solicitar_fecha():
    while True:
        fecha = input("Fecha de ingreso (DD/MM/AAAA): ").strip()

        if validar_fecha(fecha):
            return fecha

        print("Fecha inválida. Ingrese una fecha real en formato DD/MM/AAAA.")


def obtener_siguiente_numero(expedientes):
    numeros = [exp["numero"] for exp in expedientes]
    return max([0, leer_ultimo_numero(), *numeros]) + 1


def leer_ultimo_numero():
    if not os.path.exists(ARCHIVO_SECUENCIA):
        if os.path.exists(ARCHIVO_RESPALDO):
            try:
                from controllers.storage import _leer_respaldo
                return _leer_respaldo()[1]
            except (OSError, UnicodeDecodeError, json.JSONDecodeError,
                    ValueError, TypeError) as error:
                raise RuntimeError(
                    "No se puede recuperar el correlativo del respaldo. "
                    "Conserve los archivos y revise el respaldo antes de continuar."
                ) from error
        return 0
    try:
        with open(ARCHIVO_SECUENCIA, "r", encoding="utf-8") as archivo:
            numero = json.load(archivo)["ultimo_numero"]
        if type(numero) is not int or numero < 0:
            raise ValueError("El correlativo no es un entero válido.")
        return numero
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as error:
        raise RuntimeError(
            "No se puede leer el último número de expediente. "
            "Conserve los archivos y revise ultimo_numero.json antes de continuar."
        ) from error


def guardar_ultimo_numero(numero):
    temporal = ARCHIVO_SECUENCIA + ".tmp"
    try:
        with open(temporal, "w", encoding="utf-8") as archivo:
            json.dump({"ultimo_numero": numero}, archivo)
        os.replace(temporal, ARCHIVO_SECUENCIA)
        return True
    except OSError as error:
        print(f"No se pudo reservar el número de expediente: {error}")
        return False


def registrar_operacion():
    global TOTAL_OPERACIONES
    TOTAL_OPERACIONES += 1