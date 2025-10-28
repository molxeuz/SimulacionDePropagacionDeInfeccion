from modelos import Simulacion

# Configuración inicial
n = int(input("\nTamaño de la matriz (ej: 5): "))
num_personas = int(input("Número de personas (ej: 5): "))

sim = Simulacion(n, num_personas, semilla=1)

while True:
    sim.ejecutar_ronda()
    opcion = input("\nContinuar (c), curar (u), agregar (a) o salir (s): ").lower()

    if opcion == "s":
        break
    elif opcion == "u":
        nombre = input("Nombre de la persona a curar (ej: p2): ")
        sim.curar(nombre)
    elif opcion == "a":
        nombre = f"p{len(sim.personas) + 1}"
        x = int(input("x: "))
        y = int(input("y: "))
        sim.agregar_persona(nombre, x, y)
