from controllers.config import TOTAL_OPERACIONES, registrar_operacion
from controllers.expedientes import (
    actualizar_expediente,
    buscar_por_nombre,
    buscar_por_numero,
    cambiar_estado_expediente,
    eliminar_expediente,
    listar_expedientes,
    mostrar_expediente,
    ordenar_por_fecha_burbuja,
    ordenar_por_numero_seleccion,
    registrar_expediente,
)
from controllers.storage import cargar_expedientes

# ============================================================
# MENÚ PRINCIPAL
# ============================================================

def mostrar_menu():
    print("\n")
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║             SISTEMA DE MESA DE PARTES DIGITAL               ║")
    print("║       Institución Educativa 'Coronel Cortegana'              ║")
    print("╠══════════════════════════════════════════════════════════════╣")
    print("║  1. Registrar expediente                                     ║")
    print("║  2. Buscar por número                                        ║")
    print("║  3. Buscar por nombre                                        ║")
    print("║  4. Listar expedientes                                       ║")
    print("║  5. Ordenar por fecha (Burbuja)                              ║")
    print("║  6. Ordenar por número (Selección)                           ║")
    print("║  7. Actualizar datos de expediente                           ║")
    print("║  8. Cambiar estado del expediente                            ║")
    print("║  9. Eliminar expediente                                      ║")
    print("║ 10. Salir                                                    ║")
    print("╚══════════════════════════════════════════════════════════════╝")


# ============================================================
# FUNCIÓN PRINCIPAL
# ============================================================

def main():
    expedientes = cargar_expedientes()

    print("\nSistema iniciado correctamente.")
    print(f"Expedientes cargados: {len(expedientes)}")

    opcion = ""

    while opcion != "10":
        mostrar_menu()

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            registrar_expediente(expedientes)

        elif opcion == "2":
            try:
                numero = int(input("Ingrese el número de expediente: "))
                resultado = buscar_por_numero(expedientes, numero)

                if resultado is None:
                    print("No se encontró ningún expediente con ese número.")
                else:
                    mostrar_expediente(resultado)

                registrar_operacion()

            except ValueError:
                print("Debe ingresar un número válido.")

        elif opcion == "3":
            texto = input("Ingrese el nombre o parte de él: ").strip()

            resultados = buscar_por_nombre(expedientes, texto)

            if len(resultados) == 0:
                print("No se encontraron coincidencias.")
            else:
                print(f"\nSe encontraron {len(resultados)} expediente(s).")

                for exp in resultados:
                    mostrar_expediente(exp)

            registrar_operacion()

        elif opcion == "4":
            listar_expedientes(expedientes)
            registrar_operacion()

        elif opcion == "5":
            ordenados = ordenar_por_fecha_burbuja(expedientes)

            print("\nExpedientes ordenados por fecha (más antiguo primero):")
            listar_expedientes(ordenados)

            registrar_operacion()

        elif opcion == "6":
            ordenados = ordenar_por_numero_seleccion(expedientes)

            print("\nExpedientes ordenados por número:")
            listar_expedientes(ordenados)

            registrar_operacion()

        elif opcion == "7":
            actualizar_expediente(expedientes)

        elif opcion == "8":
            cambiar_estado_expediente(expedientes)

        elif opcion == "9":
            eliminar_expediente(expedientes)

        elif opcion == "10":
            print("\nSaliendo del sistema...")
            print(f"Operaciones realizadas durante esta sesión: {TOTAL_OPERACIONES}")
            print("Los datos guardados se conservarán para la próxima ejecución.")
            print("¡Hasta pronto!")

        else:
            print("Opción no válida. Seleccione una opción del 1 al 10.")


# ============================================================
# PUNTO DE ENTRADA DEL PROGRAMA
# ============================================================

if __name__ == "__main__":
    main()