from datetime import datetime
from controllers.config import (
    ESTADOS_VALIDOS,
    TIPOS_TRAMITE_VALIDOS,
    guardar_ultimo_numero,
    leer_ultimo_numero,
    limpiar_texto,
    obtener_siguiente_numero,
    registrar_operacion,
    solicitar_celular,
    solicitar_dni,
    solicitar_fecha,
    solicitar_texto,
    validar_celular,
    validar_correo,
    validar_dni,
    validar_fecha,
)
from controllers.storage import guardar_expedientes

# ============================================================
# REGISTRO DE EXPEDIENTES
# ============================================================

def registrar_expediente(expedientes):
    print("\n========== REGISTRAR EXPEDIENTE ==========")

    nombre = solicitar_texto("Nombre completo del solicitante: ")

    print("\nTipos de trámite disponibles:")
    for tipo in TIPOS_TRAMITE_VALIDOS:
        print(f"- {tipo.capitalize()}")

    tipo_tramite = input("\nTipo de trámite: ").strip().lower()

    while tipo_tramite not in TIPOS_TRAMITE_VALIDOS:
        print("Tipo de trámite no válido.")
        tipo_tramite = input("Ingrese nuevamente el tipo de trámite: ").strip().lower()

    if tipo_tramite == "certificado":
        dni = solicitar_dni(obligatorio=True)
    else:
        dni = solicitar_dni(obligatorio=False)

    fecha = solicitar_fecha()
    celular = solicitar_celular()

    correo = limpiar_texto(input("Correo electrónico (opcional): "))

    while not validar_correo(correo):
        print("El correo ingresado no tiene un formato válido.")
        correo = limpiar_texto(input("Ingrese nuevamente el correo: "))

    descripcion = solicitar_texto("Descripción del pedido o asunto: ")

    numero = obtener_siguiente_numero(expedientes)
    if not guardar_ultimo_numero(numero):
        print("Se canceló el registro para evitar reutilizar el número.")
        return

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

    if guardar_expedientes(expedientes):
        registrar_operacion()
        print("\nExpediente registrado correctamente.")
        print(f"Número asignado: {numero}")
    else:
        print("El registro no se completó en ambos archivos. "
              "Revise los mensajes anteriores antes de cerrar.")


# ============================================================
# PRESENTACIÓN Y BÚSQUEDA DE EXPEDIENTES
# ============================================================

def mostrar_expediente(exp):
    print("\n" + "-" * 55)
    print(f"N° de expediente : {exp['numero']}")
    print(f"Solicitante      : {exp['nombre']}")
    print(f"DNI              : {exp['dni'] if exp['dni'] else 'No registrado'}")
    print(f"Tipo de trámite  : {exp['tipo_tramite'].capitalize()}")
    print(f"Fecha de ingreso : {exp['fecha']}")
    print(f"Celular          : {exp['celular']}")
    print(f"Correo           : {exp['correo'] if exp['correo'] else 'No registrado'}")
    print(f"Descripción      : {exp['descripcion']}")
    print(f"Estado           : {exp['estado'].capitalize()}")
    print("-" * 55)


def buscar_por_numero(expedientes, numero):
    for exp in expedientes:
        if exp["numero"] == numero:
            return exp

    return None


def buscar_por_nombre(expedientes, texto_buscado):
    """
    Busca coincidencias parciales sin distinguir
    entre mayúsculas y minúsculas.
    """

    resultados = []

    texto_buscado = texto_buscado.strip().lower()

    if texto_buscado == "":
        return resultados

    for exp in expedientes:
        nombre_normalizado = exp["nombre"].lower()

        if texto_buscado in nombre_normalizado:
            resultados.append(exp)

    return resultados


# ============================================================
# LISTADO Y RESUMEN DE EXPEDIENTES
# ============================================================

def contar_recursivamente(expedientes, estado=None, indice=0):
    """
    Cuenta expedientes utilizando recursividad.
    El caso base se alcanza cuando se llega al final
    de la lista.
    """

    if indice >= len(expedientes):
        return 0

    coincide = (
        estado is None
        or expedientes[indice]["estado"] == estado
    )

    cantidad_actual = 1 if coincide else 0

    return cantidad_actual + contar_recursivamente(
        expedientes,
        estado,
        indice + 1
    )


def mostrar_resumen(expedientes):
    """
    Utiliza arreglos paralelos y una matriz bidimensional
    para resumir los expedientes por trámite y estado.
    """

    tipos = TIPOS_TRAMITE_VALIDOS.copy()
    totales_por_tipo = [0] * len(tipos)

    estados = ESTADOS_VALIDOS.copy()

    matriz = [
        [0 for estado in estados]
        for tipo in tipos
    ]

    for exp in expedientes:
        if exp["tipo_tramite"] in tipos:
            fila = tipos.index(exp["tipo_tramite"])
            totales_por_tipo[fila] += 1

            if exp["estado"] in estados:
                columna = estados.index(exp["estado"])
                matriz[fila][columna] += 1

    print("\n========== RESUMEN DE EXPEDIENTES ==========")

    print(f"Total de expedientes: {contar_recursivamente(expedientes)}")

    for estado in estados:
        cantidad = contar_recursivamente(expedientes, estado)
        print(f"Expedientes {estado}: {cantidad}")

    print("\nCantidad por tipo de trámite:")

    for i in range(len(tipos)):
        print(f"{tipos[i].capitalize():20} : {totales_por_tipo[i]}")

    print("\nMATRIZ DE EXPEDIENTES POR TRÁMITE Y ESTADO")
    print(f"{'Tipo de trámite':20} {'Registrado':12} {'En proceso':12} {'Entregado':12}")

    for i in range(len(tipos)):
        print(
            f"{tipos[i].capitalize():20} "
            f"{matriz[i][0]:12} "
            f"{matriz[i][1]:12} "
            f"{matriz[i][2]:12}"
        )


def listar_expedientes(expedientes):
    if len(expedientes) == 0:
        print("\nNo hay expedientes registrados.")
        return

    print(f"\n========== LISTADO DE EXPEDIENTES ({len(expedientes)}) ==========")

    for exp in expedientes:
        mostrar_expediente(exp)

    mostrar_resumen(expedientes)


# ============================================================
# ORDENAMIENTOS: BURBUJA Y SELECCIÓN
# ============================================================

def ordenar_por_fecha_burbuja(expedientes):
    """
    Ordenamiento burbuja por fecha.
    Se utiliza una copia para no modificar
    el orden original de la lista.
    """

    lista = expedientes.copy()
    n = len(lista)

    for i in range(n - 1):
        hubo_cambios = False

        for j in range(n - 1 - i):
            fecha_actual = datetime.strptime(
                lista[j]["fecha"], "%d/%m/%Y"
            )

            fecha_siguiente = datetime.strptime(
                lista[j + 1]["fecha"], "%d/%m/%Y"
            )

            if fecha_actual > fecha_siguiente:
                lista[j], lista[j + 1] = lista[j + 1], lista[j]
                hubo_cambios = True

        if not hubo_cambios:
            break

    return lista


def ordenar_por_numero_seleccion(expedientes):
    """
    Ordenamiento por selección.
    Busca el menor número y lo coloca
    en la posición correspondiente.
    """

    lista = expedientes.copy()
    n = len(lista)

    for i in range(n - 1):
        indice_menor = i

        for j in range(i + 1, n):
            if lista[j]["numero"] < lista[indice_menor]["numero"]:
                indice_menor = j

        if indice_menor != i:
            lista[i], lista[indice_menor] = lista[indice_menor], lista[i]

    return lista


# ============================================================
# ACTUALIZACIÓN DE EXPEDIENTES
# ============================================================

def actualizar_expediente(expedientes):
    print("\n========== ACTUALIZAR EXPEDIENTE ==========")

    try:
        numero = int(input("Número de expediente: "))
    except ValueError:
        print("Debe ingresar un número válido.")
        return

    exp = buscar_por_numero(expedientes, numero)

    if exp is None:
        print("No se encontró el expediente.")
        return

    mostrar_expediente(exp)

    print("\nPresione Enter para conservar el dato actual.")

    nuevo_nombre = input(
        f"Nombre [{exp['nombre']}]: "
    ).strip()

    if nuevo_nombre:
        nuevo_nombre = limpiar_texto(nuevo_nombre)

    nuevo_dni = input(
        f"DNI [{exp['dni']}]: "
    ).strip()

    if nuevo_dni != "" and not validar_dni(nuevo_dni):
        print("El DNI debe tener 8 dígitos.")
        return

    nueva_fecha = input(
        f"Fecha [{exp['fecha']}]: "
    ).strip()

    if nueva_fecha != "" and not validar_fecha(nueva_fecha):
        print("La fecha ingresada no es válida.")
        return

    nuevo_celular = input(
        f"Celular [{exp['celular']}]: "
    ).strip()

    if nuevo_celular != "" and not validar_celular(nuevo_celular):
        print("El celular debe tener 9 dígitos.")
        return

    nuevo_correo = input(
        f"Correo [{exp['correo']}]: "
    ).strip()

    if nuevo_correo != "" and not validar_correo(nuevo_correo):
        print("El correo ingresado no es válido.")
        return

    nueva_descripcion = input(
        f"Descripción [{exp['descripcion']}]: "
    ).strip()

    # Los cambios se aplican después de validar los datos.
    if nuevo_nombre:
        exp["nombre"] = nuevo_nombre

    if nuevo_dni:
        exp["dni"] = nuevo_dni

    if nueva_fecha:
        exp["fecha"] = nueva_fecha

    if nuevo_celular:
        exp["celular"] = nuevo_celular

    if nuevo_correo:
        exp["correo"] = limpiar_texto(nuevo_correo)

    if nueva_descripcion:
        exp["descripcion"] = limpiar_texto(nueva_descripcion)

    if guardar_expedientes(expedientes):
        registrar_operacion()
        print("Los datos del expediente fueron actualizados correctamente.")
    else:
        print("La actualización no se confirmó en ambos archivos.")


# ============================================================
# CAMBIO DE ESTADO
# ============================================================

def cambiar_estado_expediente(expedientes):
    print("\n========== CAMBIAR ESTADO ==========")

    try:
        numero = int(input("Número de expediente: "))
    except ValueError:
        print("Debe ingresar un número válido.")
        return

    exp = buscar_por_numero(expedientes, numero)

    if exp is None:
        print("No se encontró el expediente.")
        return

    print(f"\nEstado actual: {exp['estado']}")

    print("\nEstados disponibles:")
    for i, estado in enumerate(ESTADOS_VALIDOS, start=1):
        print(f"{i}. {estado.capitalize()}")

    try:
        opcion = int(input("Seleccione el nuevo estado: "))
    except ValueError:
        print("Debe ingresar una opción numérica.")
        return

    if opcion < 1 or opcion > len(ESTADOS_VALIDOS):
        print("Opción de estado no válida.")
        return

    nuevo_estado = ESTADOS_VALIDOS[opcion - 1]

    if nuevo_estado == exp["estado"]:
        print("El expediente ya tiene ese estado.")
        return

    exp["estado"] = nuevo_estado

    if guardar_expedientes(expedientes):
        registrar_operacion()
        print(f"Estado actualizado a: {nuevo_estado.capitalize()}")
    else:
        print("El cambio de estado no se confirmó en ambos archivos.")


# ============================================================
# ELIMINACIÓN DE EXPEDIENTES
# ============================================================

def eliminar_expediente(expedientes):
    print("\n========== ELIMINAR EXPEDIENTE ==========")

    try:
        numero = int(input("Número de expediente: "))
    except ValueError:
        print("Debe ingresar un número válido.")
        return

    exp = buscar_por_numero(expedientes, numero)

    if exp is None:
        print("No se encontró el expediente.")
        return

    mostrar_expediente(exp)

    confirmacion = input(
        "¿Está seguro de eliminar este expediente? (S/N): "
    ).strip().lower()

    if confirmacion == "s":
        ultimo = max([leer_ultimo_numero(),
                      *(item["numero"] for item in expedientes)])
        if not guardar_ultimo_numero(ultimo):
            print("Se canceló la eliminación para conservar el correlativo.")
            return
        expedientes.remove(exp)

        if guardar_expedientes(expedientes):
            registrar_operacion()
            print("Expediente eliminado correctamente.")
        else:
            print("La eliminación no se confirmó en ambos archivos.")
    else:
        print("Operación cancelada.")