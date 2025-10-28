import random
from typing import List, Optional, Dict


# ==============================
# 🧍 CLASE PERSONA
# ==============================
class Persona:
    def __init__(self, nombre: str, x: int, y: int, defensa: int = 3):
        self.nombre = nombre
        self.x = x
        self.y = y
        self.defensa = defensa
        self.infectado = False

    def mover(self, n: int) -> None:
        dx = random.choice([-1, 0, 1])
        dy = random.choice([-1, 0, 1])

        # Movimiento provisional
        nuevo_x = self.x + dx
        nuevo_y = self.y + dy

        # Rebote en bordes
        if nuevo_x < 0 or nuevo_x >= n:
            dx *= -1
            nuevo_x = self.x + dx
        if nuevo_y < 0 or nuevo_y >= n:
            dy *= -1
            nuevo_y = self.y + dy

        # Actualizar posición
        self.x = nuevo_x
        self.y = nuevo_y


    def __str__(self) -> str:
        icono = "🟥" if self.infectado else "🟩"
        return f"{icono}{self.nombre}({self.defensa})"


# ==============================
# 🌳 CLASE ÁRBOL DE CONTAGIO
# ==============================
class ArbolContagio:
    def __init__(self):
        self.contagios: Dict[str, List[str]] = {}

    def agregar_contagio(self, infectador: str, infectado: str) -> None:
        if infectador not in self.contagios:
            self.contagios[infectador] = []
        self.contagios[infectador].append(infectado)

    def eliminar_persona(self, persona: str) -> None:
        for infectador, hijos in self.contagios.items():
            if persona in hijos:
                hijos.remove(persona)
                if persona in self.contagios:
                    hijos.extend(self.contagios[persona])
        self.contagios.pop(persona, None)

    def mostrar(self) -> None:
        print("\n🌳 Árbol de contagio:")
        if not self.contagios:
            print("  (Vacío)")
        else:
            for inf, hijos in self.contagios.items():
                print(f"  {inf} → {', '.join(hijos) if hijos else '(sin contagios)'}")


# ==============================
# 🧭 CLASE MATRIZ
# ==============================
class Matriz:
    def __init__(self, n: int):
        self.n = n
        self.celdas = [["." for _ in range(n)] for _ in range(n)]

    def limpiar(self) -> None:
        self.celdas = [["." for _ in range(self.n)] for _ in range(self.n)]

    def actualizar(self, personas: List[Persona]) -> None:
        self.limpiar()
        for p in personas:
            if self.celdas[p.x][p.y] == ".":
                self.celdas[p.x][p.y] = p.nombre
            else:
                # mostrar múltiples personas en una celda
                self.celdas[p.x][p.y] += f"/{p.nombre}"

    def mostrar(self, personas: List[Persona]) -> None:
        print("\n🗺️  MATRIZ DE SIMULACIÓN")
        print("   " + " ".join([f"{i:3}" for i in range(self.n)]))
        print("   " + "―" * (self.n * 4))

        for i in range(self.n):
            fila = []
            for j in range(self.n):
                ocupantes = [p for p in personas if p.x == i and p.y == j]
                if ocupantes:
                    if len(ocupantes) > 1:
                        fila.append("⚠️ ")
                    else:
                        icono = "🟥" if ocupantes[0].infectado else "🟩"
                        fila.append(f"{icono}")
                else:
                    fila.append("⬜")
            print(f"{i:2}| " + "  ".join(fila))
        print()


# ==============================
# 🧠 CLASE SIMULACIÓN
# ==============================
class Simulacion:
    def __init__(self, n: int, num_personas: int, semilla: Optional[int] = None):
        if semilla is not None:
            random.seed(semilla)

        self.n = n
        self.matriz = Matriz(n)
        self.personas: List[Persona] = []
        self.arbol = ArbolContagio()
        self.ronda = 0

        # Crear personas
        for i in range(num_personas):
            x, y = random.randint(0, n - 1), random.randint(0, n - 1)
            self.personas.append(Persona(f"p{i+1}", x, y))

        # Elegir paciente cero
        paciente_cero = random.choice(self.personas)
        paciente_cero.infectado = True
        self.arbol.contagios[paciente_cero.nombre] = []

    # --- Dinámica ---
    def mover_personas(self) -> None:
        for p in self.personas:
            p.mover(self.n)

    def revisar_contagios(self) -> None:
        for p_sana in self.personas:
            if not p_sana.infectado:
                infectados_en_celda = [
                    p for p in self.personas
                    if p.x == p_sana.x and p.y == p_sana.y and p.infectado
                ]
                if infectados_en_celda:
                    p_sana.defensa -= len(infectados_en_celda)
                    if p_sana.defensa <= 0:
                        p_sana.infectado = True
                        infectador = random.choice(infectados_en_celda)
                        self.arbol.agregar_contagio(infectador.nombre, p_sana.nombre)

    def aumentar_defensas(self) -> None:
        if self.ronda % 3 == 0 and self.ronda > 0:
            for p in self.personas:
                if not p.infectado:
                    p.defensa += 1

    # --- Acciones del usuario ---
    def curar(self, nombre: str) -> None:
        for p in self.personas:
            if p.nombre == nombre and p.infectado:
                p.infectado = False
                p.defensa = 3
                self.arbol.eliminar_persona(nombre)
                print(f"✅ {nombre} ha sido curado.")
                return
        print("⚠️ No se encontró o no estaba infectado.")

    def agregar_persona(self, nombre: str, x: int, y: int) -> None:
        nueva = Persona(nombre, x, y)
        self.personas.append(nueva)
        print(f"👤 Se ha agregado {nombre} en posición ({x}, {y}).")

    # --- Visualización ---
    def mostrar_estado(self) -> None:
        sanas = [p for p in self.personas if not p.infectado]
        infectadas = [p for p in self.personas if p.infectado]

        print("\n💚 Sanas:")
        for s in sanas:
            print(f"  {s.nombre} (defensa={s.defensa})")

        print("\n💀 Infectadas:")
        for i in infectadas:
            print(f"  {i.nombre}")

        self.arbol.mostrar()

    def ejecutar_ronda(self) -> None:
        self.ronda += 1
        print(f"\n===== 🌀 RONDA {self.ronda} =====")
        self.mover_personas()
        self.revisar_contagios()
        self.aumentar_defensas()
        self.matriz.actualizar(self.personas)
        self.matriz.mostrar(self.personas)
        self.mostrar_estado()
