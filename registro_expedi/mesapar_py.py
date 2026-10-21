"""
- MODELO DE INTERFAZ PARA TERMINAL
  MESCORT (Por MESa de partes y el colegio Coronel CORTegana)
  ┌──────────────────────────────────────────────────────────────┐
  │             SISTEMA DE MESA DE PARTES DIGITAL                │
  │    Institución Educativa "Coronel Cortegana" - Celendín      │
  └──────────────────────────────────────────────────────────────┘
  ==============================================================═╗
          [+] Registrar expedientes (con validación)
          [?] Buscar expedientes (por número / nombre)
          [↑↓] Ordenar expedientes (burbuja / selección)
          [✓] Marcar expedientes como entregados
          [⬡] Guardar y recuperar desde archivo de texto
  ╚==============================================================
"""

import os

ARCHIVO_DATOS = "expedientes.txt"
SEPARADOR = "|" 

TIPOS_TRAMITE_VALIDOS = [
    "certificado", "permiso", "reclamo", "comunicacion",
    "tesoreria", "informe de salud", "apoyo"
]

def cargar_expedientes(): # Lee el archivo de texto y reconstruye la lista de expedientes.
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


def guardar_expedientes(expedientes): # Escribe TODA la lista de expedientes en el archivo de texto.
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


def validar_texto_no_vacio(texto): #Devuelve True si el texto tiene contenido real (no solo espacios).
    return texto.strip() != ""


def validar_dni(dni): #El DNI solo es obligatorio para certificados, por eso esta función se usa condicionalmente, no siempre.
    return dni.isdigit() and len(dni) == 8

def validar_celular(celular): #Un celular válido en Perú tiene 9 dígitos numéricos.
    return celular.isdigit() and len(celular) == 9


def obtener_siguiente_numero(expedientes): # Calcula el siguiente número de expediente correlativo como el cuaderno de la secretaria.
    if len(expedientes) == 0:
        return 1
    numeros = [exp["numero"] for exp in expedientes]
    return max(numeros) + 1


def registrar_expediente(expedientes): # Pide los datos de un nuevo trámite, los valida y agrega el nuevo expediente a la lista.
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

def mostrar_expediente(exp): #Imprime en pantalla los datos de un solo expediente.
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

def buscar_por_numero(expedientes, numero): # Búsqueda por número de expediente
    for exp in expedientes:
        if exp["numero"] == numero:
            return exp
    return None

def buscar_por_nombre(expedientes, texto_buscado): # Búsqueda por coincidencia parcial de nombre.
    resultados = []
    texto_buscado = texto_buscado.lower()
    for exp in expedientes:
        if texto_buscado in exp["nombre"].lower():
            resultados.append(exp)
    return resultados

def ordenar_por_fecha_burbuja(expedientes): # Algoritmo de ordenamiento BURBUJA, que ordena los expedientes por fecha de ingreso.
    lista = expedientes.copy()
    n = len(lista)

    def clave_fecha(exp):
        dia, mes, anio = exp["fecha"].split("/")
        return anio + mes + dia

    for i in range(n - 1):
        for j in range(n - 1 - i):
            if clave_fecha(lista[j]) > clave_fecha(lista[j + 1]):
                lista[j], lista[j + 1] = lista[j + 1], lista[j]

    return lista

def ordenar_por_numero_seleccion(expedientes): # Algoritmo de ordenamiento por SELECCIÓN, que ordena los expedientes por número.
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

def listar_expedientes(expedientes): # Muestra todos los expedientes registrados
    if len(expedientes) == 0:
        print("\nNo hay expedientes registrados todavía.")
        return

    print(f"\n--- LISTADO DE EXPEDIENTES ({len(expedientes)} en total) ---")
    for exp in expedientes:
        mostrar_expediente(exp)

def marcar_como_entregado(expedientes, numero):# Marca un expediente como entregado
    exp = buscar_por_numero(expedientes, numero)
    if exp is None:
        return False
    exp["estado"] = "entregado"
    guardar_expedientes(expedientes)
    return True

def mostrar_menu(): #Diseño de la interfaz de menú principal con arte ASCII.
    print(r"")
    print(r"███╗   ███╗███████╗███████╗ ██████╗  ██████╗ ██████╗ ████████╗")
    print(r"████╗ ████║██╔════╝██╔════╝██╔════╝ ██╔═══██╗██╔══██╗╚══██╔══╝")
    print(r"██╔████╔██║█████╗  ███████╗██║      ██║   ██║██████╔╝   ██║   ")
    print(r"██║╚██╔╝██║██╔══╝  ╚════██║██║      ██║   ██║██╔══██╗   ██║   ")
    print(r"██║ ╚═╝ ██║███████╗███████║╚██████╗ ╚██████╔╝██║  ██║   ██║   ")
    print(r"╚═╝     ╚═╝╚══════╝╚══════╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ")
    print(r"")
    print(r"┌──────────────────────────────────────────────────────────────┐")
    print(r"│              SISTEMA DE MESA DE PARTES DIGITAL               │")
    print(r"│      Institución Educativa ""Coronel Cortegana"" - Celendín  ⯏   │")
    print(r"└──────────────────────────────────────────────────────────────┘")
    print(r"")
    print(r"𒋲═══════════════════════════════════════════════════════════╗")
    print(r"     ★ [ + ] 1. Registrar expedientes                        ")
    print(r"     ★ [ ? ] 2. Buscar expedientes                           ")
    print(r"     ★ [↑ ↓] 3. Ordenar expedientes                         ")
    print(r"     ★ [ ✓ ] 4. Marcar expedientes como entregados           ")
    print(r"     ★ [ ⬡ ] 5. Guardar y recuperar desde archivo de texto   ")
    print(r"╚═══════════════════════════════════════════════════════════𒋲")


def main():
    expedientes = cargar_expedientes()
    opcion = ""

    while opcion != "8":
        mostrar_menu()
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            registrar_expediente(expedientes)

        elif opcion == "2":
            try:
                numero = int(input("Ingrese el número de expediente: "))
            except ValueError:
                print("Debe ingresar un número válido.")
                continue
            resultado = buscar_por_numero(expedientes, numero)
            if resultado is None:
                print("No se encontró ningún expediente con ese número.")
            else:
                mostrar_expediente(resultado)

        elif opcion == "3":
            texto = input("Ingrese el nombre (o parte de él): ")
            resultados = buscar_por_nombre(expedientes, texto)
            if len(resultados) == 0:
                print("No se encontraron expedientes con ese nombre.")
            else:
                print(f"\nSe encontraron {len(resultados)} expediente(s):")
                for exp in resultados:
                    mostrar_expediente(exp)

        elif opcion == "4":
            listar_expedientes(expedientes)

        elif opcion == "5":
            ordenados = ordenar_por_fecha_burbuja(expedientes)
            print("\nExpedientes ordenados por fecha (más antiguo primero):")
            listar_expedientes(ordenados)

        elif opcion == "6":
            ordenados = ordenar_por_numero_seleccion(expedientes)
            print("\nExpedientes ordenados por número:")
            listar_expedientes(ordenados)

        elif opcion == "7":
            try:
                numero = int(input("Ingrese el número de expediente a marcar como entregado: "))
            except ValueError:
                print("Debe ingresar un número válido.")
                continue
            if marcar_como_entregado(expedientes, numero):
                print("Expediente marcado como entregado.")
            else:
                print("No se encontró ningún expediente con ese número.")

        elif opcion == "8":
            print("\nSaliendo del sistema. ¡Hasta pronto!")

        else:
            print("Opción no válida, intente nuevamente.")


if __name__ == "__main__":
    main()