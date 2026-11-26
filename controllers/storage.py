import json
import os
import shutil
from datetime import datetime

from controllers.config import (
    ARCHIVO_DATOS,
    ARCHIVO_RESPALDO,
    SEPARADOR,
    guardar_ultimo_numero,
    leer_ultimo_numero,
    validar_fecha,
)

# ============================================================
# PERSISTENCIA DE DATOS: ARCHIVOS DE TEXTO Y BINARIOS
# ============================================================

def _escribir_atomico(ruta, contenido, modo="w"):
    temporal = ruta + ".tmp"
    with open(temporal, modo, **({"encoding": "utf-8"} if modo == "w" else {})) as archivo:
        archivo.write(contenido)
    os.replace(temporal, ruta)


def guardar_expedientes(expedientes):
    """Guarda el archivo principal y el respaldo. Devuelve True si ambos se guardaron."""
    lineas = []
    for exp in expedientes:
        campos = [
            str(exp["numero"]), exp["nombre"], exp["dni"], exp["tipo_tramite"],
            exp["fecha"], exp["celular"], exp["correo"], exp["descripcion"],
            exp["estado"]
        ]
        if any(SEPARADOR in campo or "\n" in campo or "\r" in campo for campo in campos):
            print("No se guardó: hay un campo con un separador o salto de línea.")
            return False
        lineas.append(SEPARADOR.join(campos))

    try:
        _escribir_atomico(ARCHIVO_DATOS, "".join(linea + "\n" for linea in lineas))
    except OSError as error:
        print(f"No se pudieron guardar los expedientes: {error}")
        return False

    if not crear_respaldo_binario(expedientes):
        print("Se guardó el archivo principal, pero falló el respaldo.")
        return False
    return True


def crear_respaldo_binario(expedientes):
    """Guarda JSON codificado como bytes y conserva el mayor número asignado."""
    try:
        ultimo = max([leer_ultimo_numero(), *(exp["numero"] for exp in expedientes)])
        contenido = json.dumps(
            {"ultimo_numero": ultimo, "expedientes": expedientes},
            ensure_ascii=False
        ).encode("utf-8")
        _escribir_atomico(ARCHIVO_RESPALDO, contenido, "wb")
        return True
    except (OSError, TypeError, ValueError, RuntimeError) as error:
        print(f"No se pudo crear el respaldo binario: {error}")
        return False


def _validar_expediente(exp):
    campos = ("numero", "nombre", "dni", "tipo_tramite", "fecha",
              "celular", "correo", "descripcion", "estado")
    return (
        isinstance(exp, dict)
        and all(campo in exp for campo in campos)
        and type(exp["numero"]) is int and exp["numero"] > 0
        and all(isinstance(exp[campo], str) for campo in campos[1:])
        and validar_fecha(exp["fecha"])
    )


def _leer_respaldo():
    with open(ARCHIVO_RESPALDO, "rb") as archivo:
        datos = json.loads(archivo.read().decode("utf-8"))
    # El respaldo anterior contenía directamente la lista.
    if isinstance(datos, list):
        expedientes = datos
        if any(not isinstance(exp, dict) for exp in expedientes):
            raise ValueError("La lista del respaldo contiene un registro inválido.")
        ultimo = max([0, *(exp.get("numero", 0) for exp in expedientes)])
    elif isinstance(datos, dict):
        expedientes = datos.get("expedientes")
        ultimo = datos.get("ultimo_numero")
    else:
        raise ValueError("Formato de respaldo no reconocido.")
    if not isinstance(expedientes, list) or type(ultimo) is not int or ultimo < 0:
        raise ValueError("Estructura del respaldo no válida.")
    if any(not _validar_expediente(exp) for exp in expedientes):
        raise ValueError("Hay expedientes inválidos en el respaldo.")
    numeros = [exp["numero"] for exp in expedientes]
    if len(numeros) != len(set(numeros)) or ultimo < max([0, *numeros]):
        raise ValueError("Números duplicados o correlativo inválido en el respaldo.")
    return expedientes, ultimo


def restaurar_respaldo_binario():
    if not os.path.exists(ARCHIVO_RESPALDO):
        return None
    try:
        return _leer_respaldo()
    except (OSError, UnicodeDecodeError, json.JSONDecodeError, ValueError, TypeError) as error:
        print(f"No se pudo recuperar el respaldo binario: {error}")
        return None


def cargar_expedientes():
    """Recupera datos sin descartar filas dañadas ni sobrescribir el original."""
    if not os.path.exists(ARCHIVO_DATOS):
        recuperado = restaurar_respaldo_binario()
        if recuperado is None:
            if os.path.exists(ARCHIVO_RESPALDO):
                raise RuntimeError("Respaldo ilegible. Conserve los archivos y revise los datos.")
            return []
        expedientes, ultimo = recuperado
        if not guardar_ultimo_numero(max(leer_ultimo_numero(), ultimo)):
            raise RuntimeError("No se pudo restaurar el correlativo.")
        if not guardar_expedientes(expedientes):
            raise RuntimeError("No se pudo restaurar el archivo principal y su respaldo.")
        print("Datos recuperados del respaldo binario.")
        return expedientes

    expedientes = []
    errores = 0
    try:
        with open(ARCHIVO_DATOS, "r", encoding="utf-8") as archivo:
            for linea in archivo:
                if not linea.strip():
                    continue
                campos = linea.rstrip("\r\n").split(SEPARADOR)
                if len(campos) != 9:
                    errores += 1
                    continue
                try:
                    exp = {
                        "numero": int(campos[0]), "nombre": campos[1],
                        "dni": campos[2], "tipo_tramite": campos[3],
                        "fecha": campos[4], "celular": campos[5],
                        "correo": campos[6], "descripcion": campos[7],
                        "estado": campos[8]
                    }
                except ValueError:
                    errores += 1
                    continue
                if not _validar_expediente(exp):
                    errores += 1
                    continue
                expedientes.append(exp)
    except (OSError, UnicodeDecodeError) as error:
        raise RuntimeError(f"No se pudo leer el archivo principal: {error}") from error

    numeros = [exp["numero"] for exp in expedientes]
    if len(numeros) != len(set(numeros)):
        errores += 1

    if not errores:
        return expedientes

    print(f"Advertencia: se encontraron {errores} filas o identificadores dañados.")
    recuperado = restaurar_respaldo_binario()
    if recuperado is None:
        raise RuntimeError(
            "No hay respaldo válido. El archivo original se conservó sin cambios. "
            "Revise expedientes.txt antes de volver a iniciar."
        )
    restaurados, ultimo = recuperado
    if not set(numeros).issubset({exp["numero"] for exp in restaurados}):
        raise RuntimeError(
            "El respaldo no incluye todos los expedientes legibles del archivo principal. "
            "Ambos archivos se conservaron para revisión."
        )
    copia = ARCHIVO_DATOS + ".corrupto." + datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    try:
        shutil.copy2(ARCHIVO_DATOS, copia)
    except OSError as error:
        raise RuntimeError(f"No se pudo preservar el archivo dañado: {error}") from error
    if not guardar_ultimo_numero(max(leer_ultimo_numero(), ultimo, *numeros)):
        raise RuntimeError(f"El original se preservó en {copia}, pero no se restauró el correlativo.")
    if not guardar_expedientes(restaurados):
        raise RuntimeError(f"El original se preservó en {copia}, pero falló la restauración.")
    print(f"Se recuperó el respaldo. El archivo original se conservó en {copia}.")
    return restaurados