
from modelos import Simulacion

# ===================================================
#*   sEJECUCIÓN DE LA SIMULACIÓN
# ===================================================

def pedir_entero(mensaje: str) -> int:
    """Solicita un número entero al usuario"""
    while True:
        try:
            return int(input(mensaje))
        except ValueError:
            print("Por favor ingrese un numero valido.")

def main() -> None:
    """Ejecuta la simulación desde consola."""

    print("\n=== SIMULADOR DE CONTAGIO ===")

    n = pedir_entero("\nTamaño de la matriz (ej: 5): ")
    num_personas = pedir_entero("Número de personas (ej: 5): ")

    sim = Simulacion(n, num_personas)

    while True:
        sim.ejecutar_ronda()

        opcion = input("\nContinuar (c), curar (u), agregar (a) o salir (s): ").lower()

        if opcion == "s":
            print("\nSimulación finalizada. 👋")
            break

        elif opcion == "u":
            nombre = input("Nombre de la persona a curar (ej: p2): ")
            sim.curar_persona(nombre)

        elif opcion == "a":
            nombre = f"p{len(sim.personas) + 1}"
            x = pedir_entero("x: ")
            y = pedir_entero("y: ")
            sim.agregar_persona(nombre, x, y)

        elif opcion == "c":
            continue
        else:
            print("Opción no reconocida. Usa c, u, a o s.")

if __name__ == "__main__":
    main()