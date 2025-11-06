
"""simulacion.py"""

from modelos import Simulacion  # Importa la clase Simulacion definida en el archivo modelos.py

# ===================================================
#*   EJECUCIÓN DE LA SIMULACIÓN
# ===================================================

def pedir_entero(mensaje: str) -> int:
    """Solicita un número entero al usuario y valida la entrada."""
    while True:
        try:
            # Intenta convertir la entrada del usuario en un número entero
            return int(input(mensaje))
        except ValueError:
            # Si el usuario no ingresa un número válido, muestra un mensaje de error
            print("Por favor ingrese un numero valido.")


def main() -> None:
    """Ejecuta la simulación desde la consola."""
    print("\n=== SIMULADOR DE CONTAGIO ===")

    # Solicita al usuario el tamaño del mapa y la cantidad de personas
    n = pedir_entero("\nTamaño de la matriz (ej: 5): ")
    num_personas = pedir_entero("Número de personas (ej: 5): ")

    # Crea una instancia de la simulación con los valores ingresados
    sim = Simulacion(n, num_personas)

    # Bucle principal: se repite hasta que el usuario decida salir
    while True:
        # Ejecuta una ronda completa de la simulación
        sim.ejecutar_ronda()

        # Menú de acciones disponibles para el usuario
        opcion = input("\nContinuar (c), curar (u), agregar (a) o salir (s): ").lower()

        if opcion == "s":
            # Termina la simulación
            print("\nSimulación finalizada. 👋")
            break

        elif opcion == "u":
            # Permite curar manualmente a una persona infectada
            nombre = input("Nombre de la persona a curar (ej: p2): ")
            sim.curar_persona(nombre)

        elif opcion == "a":
            # Agrega una nueva persona en el mapa
            nombre = f"p{len(sim.personas) + 1}"  # Asigna un nombre automático (pN)
            x = pedir_entero("x: ")
            y = pedir_entero("y: ")
            sim.agregar_persona(nombre, x, y)

        elif opcion == "c":
            # Continúa directamente con la siguiente ronda
            continue
        else:
            # Controla entradas inválidas del usuario
            print("Opción no reconocida. Usa c, u, a o s.")


# Punto de entrada del programa (solo se ejecuta si el archivo es el principal)
if __name__ == "__main__":
    main()

"""modelos.py"""

# Importamos el módulo random para generar números aleatorios.
import random

# Importamos los tipos Dict y List para hacer anotaciones de tipos más claras.
from typing import Dict, List

# Fijamos una semilla para que los resultados aleatorios sean siempre iguales al ejecutar el código.
random.seed(777)

# ---------------------------------------------------
#*                     CLASE PERSONA
# ---------------------------------------------------
class Persona:
    """Representa a una persona dentro del mapa, con posición, defensa e infección."""

    # Constructor: se ejecuta al crear una nueva persona.
    def __init__(self, nombre: str, pos_x: int, pos_y: int, defensa_base: int, defensa_max: int) -> None:
        # Guarda el nombre de la persona.
        self.nombre = nombre
        # Guarda la posición horizontal (x) dentro del mapa.
        self.x = pos_x
        # Guarda la posición vertical (y) dentro del mapa.
        self.y = pos_y
        # Asigna la defensa inicial de la persona.
        self.defensa: int = defensa_base
        # Guarda el valor máximo que puede alcanzar la defensa.
        self.defensa_max: int = defensa_max
        # Inicialmente, la persona no está infectada.
        self.infectado: bool = False

    # Método que mueve a la persona a una celda adyacente de forma aleatoria.
    def mover_una_celda(self, tamaño_mapa: int) -> None:
        """Mueve la persona una celda aleatoriamente."""

        # Se elige un número aleatorio entre -1 y 1 para mover en el eje X (izquierda, quieto, derecha).
        mover_x = random.randint(-1, 1)
        # Se elige un número aleatorio entre -1 y 1 para mover en el eje Y (arriba, quieto, abajo).
        mover_y = random.randint(-1, 1)

        # Se calcula la nueva posición sumando el movimiento aleatorio a la posición actual.
        nueva_x = self.x + mover_x
        nueva_y = self.y + mover_y

        # Ajusta la nueva posición X para que no se salga del mapa.
        nueva_x = self.ajustar_posicion(nueva_x, tamaño_mapa)
        # Ajusta la nueva posición Y para que no se salga del mapa.
        nueva_y = self.ajustar_posicion(nueva_y, tamaño_mapa)

        # Actualiza la posición de la persona con las coordenadas corregidas.
        self.x = nueva_x
        self.y = nueva_y

    # Método auxiliar que evita que una coordenada salga de los límites del mapa.
    def ajustar_posicion(self, valor: int, limite: int) -> int:
        """Corrige una coordenada si está fuera del rango permitido."""
        # Si el valor es menor que 0, se devuelve 0 (borde izquierdo o superior).
        if valor < 0:
            return 0
        # Si el valor es igual o mayor al límite del mapa, se devuelve el último índice válido.
        if valor >= limite:
            return limite - 1
        # Si el valor está dentro del rango, se deja igual.
        return valor

# ---------------------------------------------------
#*              CLASE ARBOL DE CONTAGIO
# ---------------------------------------------------
class ArbolContagio:
    """Guarda los contagios ocurridos: quién contagió a quién."""

    # Constructor: inicializa el diccionario vacío de contagios.
    def __init__(self) -> None:
        # Diccionario donde la clave es el nombre del infectador y el valor es una lista de infectados.
        self.registros: Dict[str, List[str]] = {}

    # Registra un nuevo contagio entre dos personas.
    def registrar_contagio(self, infectador: str, infectado: str) -> None:
        # Si el infectador aún no tiene lista, se crea una nueva lista vacía.
        if infectador not in self.registros:
            self.registros[infectador] = []
        # Se agrega el nombre del nuevo infectado a la lista del infectador.
        self.registros[infectador].append(infectado)

    # Elimina completamente a una persona del árbol (por ejemplo, si fue curada).
    def eliminar_persona(self, persona: str) -> None:
        """Elimina a una persona del árbol de contagio."""

        # Recorre cada clave (infectador) en el diccionario.
        for clave in list(self.registros.keys()):
            # Si la persona aparece como infectada por alguien, se elimina de esa lista.
            if persona in self.registros[clave]:
                self.registros[clave].remove(persona)

        # Si la persona también era infectadora (clave del diccionario), se elimina toda su entrada.
        if persona in self.registros:
            del self.registros[persona]

    # Muestra en pantalla todos los contagios registrados.
    def mostrar_arbol(self) -> None:
        print("\nÁrbol de contagio:")
        # Si el diccionario está vacío, significa que no hay contagios.
        if not self.registros:
            print("  No hay contagios aún.")
        else:
            # Recorre cada infectador y muestra a quién contagió.
            for persona in self.registros:
                print(" ", persona, "infectó a:", self.registros[persona])

# ---------------------------------------------------
#*                 CLASE MATRIZ (EL MAPA)
# ---------------------------------------------------
class Matriz:
    """Representa el mapa cuadrado donde se mueven las personas."""

    # Constructor: define el tamaño del mapa.
    def __init__(self, tamaño: int) -> None:
        # Guarda el tamaño (por ejemplo, un mapa 10x10 tiene tamaño = 10)
        self.tamaño: int = tamaño

    # Imprime el mapa visualmente en consola.
    def imprimir_mapa(self, lista_personas: List[Persona]) -> None:
        print("\nMapa:")

        # Recorre todas las filas del mapa (eje X)
        for fila in range(self.tamaño):
            # Crea una cadena vacía para construir la fila visualmente.
            linea = ""
            # Recorre todas las columnas del mapa (eje Y)
            for col in range(self.tamaño):
                # Busca si hay personas en esta celda específica.
                personas_en_celda = self.buscar_personas_celda(lista_personas, fila, col)

                # Si no hay personas, se dibuja un cuadro blanco.
                if len(personas_en_celda) == 0:
                    linea += "⬜ "
                # Si hay más de una persona en la misma celda, se muestra un símbolo de alerta.
                elif len(personas_en_celda) > 1:
                    linea += "⚠️ "
                else:
                    # Si hay solo una persona, se revisa si está infectada o no.
                    persona = personas_en_celda[0]
                    if persona.infectado:
                        linea += "🟥 "  # Cuadro rojo = infectado
                    else:
                        linea += "🟩 "  # Cuadro verde = sano
            # Se imprime la línea completa que representa una fila del mapa.
            print(linea)

    # Busca todas las personas que están en una celda específica (x, y)
    def buscar_personas_celda(self, lista: List[Persona], x: int, y: int) -> List[Persona]:
        """Devuelve todas las personas que ocupan la posición (x, y)."""
        # Crea una lista filtrando las personas cuya posición coincida con (x, y)
        return [p for p in lista if p.x == x and p.y == y]

# ---------------------------------------------------
#*              CLASE SIMULACION GENERAL
# ---------------------------------------------------
class Simulacion:
    """Controla todo el flujo de la simulación: movimiento, contagios y estado."""

    # Constructor: prepara el mapa, las personas y las reglas iniciales.
    def __init__(self, tamaño_mapa: int, cantidad_personas: int) -> None:
        # Guarda el tamaño del mapa.
        self.tamaño: int = tamaño_mapa

        # Lista vacía donde se almacenarán las personas creadas.
        self.personas: List[Persona] = []

        # Contador de la ronda actual (inicia en 0).
        self.ronda: int = 0

        # Crea el árbol de contagios vacío.
        self.arbol: ArbolContagio = ArbolContagio()

        # Crea el mapa del tamaño indicado.
        self.mapa: Matriz = Matriz(tamaño_mapa)

        # Define los valores base y máximos de defensa según el tamaño del mapa.
        if self.tamaño >= 5:
            self.DEF_BASE = 1
            self.DEF_MAX = 2
        else:
            # En mapas pequeños, se calcula la defensa proporcionalmente al tamaño.
            self.DEF_BASE = max(1, self.tamaño // 4)
            self.DEF_MAX = max(self.DEF_BASE, self.tamaño // 2)
        
        # Crea las personas iniciales en posiciones aleatorias.
        self.crear_personas_iniciales(cantidad_personas)

        # Escoge aleatoriamente quién será el primer infectado ("paciente cero").
        self.elegir_paciente_cero()

        # Define cada cuántas rondas se da un bonus de defensa.
        self.BONUS_INTERVALO = max(4, ((self.tamaño // 2) + 1))
        # Define cuánto aumenta la defensa en cada bonus.
        self.BONUS_INC = 1 if self.tamaño < 12 else 2

    # ---------------------------------------------------
    #*              CREAR PERSONAS
    # ---------------------------------------------------
    def crear_personas_iniciales(self, cantidad: int) -> None:
        """Crea la cantidad de personas iniciales indicadas."""
        for i in range(cantidad):
            # Genera un nombre secuencial (p1, p2, p3…)
            nombre = f"p{i + 1}"
            # Genera coordenadas aleatorias dentro del mapa.
            x = random.randint(0, self.tamaño - 1)
            y = random.randint(0, self.tamaño - 1)
            # Crea un objeto Persona con sus atributos.
            nueva_persona = Persona(nombre, x, y, defensa_base=self.DEF_BASE, defensa_max=self.DEF_MAX)
            # Agrega la nueva persona a la lista general.
            self.personas.append(nueva_persona)

    def elegir_paciente_cero(self) -> None:
        """Elige al azar una persona que comenzará infectada."""
        # Escoge aleatoriamente una persona de la lista.
        paciente = random.choice(self.personas)
        # Marca a esa persona como infectada.
        paciente.infectado = True
        # Crea su registro vacío en el árbol (porque aún no ha contagiado a nadie).
        self.arbol.registros[paciente.nombre] = []

    # ---------------------------------------------------
    #*                   LÓGICA DEL JUEGO
    # ---------------------------------------------------
    def mover_todas_las_personas(self) -> None:
        """Hace que todas las personas se muevan una celda aleatoria."""
        # Recorre cada persona y llama a su método de movimiento.
        for persona in self.personas:
            persona.mover_una_celda(self.tamaño)

    def revisar_contagios(self) -> None:
        """Revisa si hay contagios en las celdas donde hay infectados."""
        for persona in self.personas:
            # Solo revisa las personas que están sanas.
            if persona.infectado is False:
                # Busca si en su misma celda hay infectados.
                infectados = self.buscar_infectados_en_misma_celda(persona)

                # Si hay infectados en la misma posición...
                if len(infectados) > 0:
                    # Pierde defensa igual al número de infectados presentes.
                    persona.defensa -= len(infectados)

                    # Si la defensa llega a 0 o menos, se contagia.
                    if persona.defensa <= 0:
                        self.infectar_persona(persona, infectados)

    def buscar_infectados_en_misma_celda(self, persona: Persona) -> List[Persona]:
        """Devuelve los infectados que están en la misma celda que la persona dada."""
        # Crea una lista con todos los que estén en la misma posición (x, y) y estén infectados.
        return [
            otro for otro in self.personas
            if (otro.x == persona.x and otro.y == persona.y and otro.infectado)
        ]

    def infectar_persona(self, persona: Persona, infectadores: List[Persona]) -> None:
        """Contagia a una persona y registra quién fue el responsable."""
        # Cambia el estado de la persona a infectada.
        persona.infectado = True
        # Escoge aleatoriamente cuál de los infectadores fue el que la contagió.
        quien_contagio = random.choice(infectadores)
        # Registra el contagio en el árbol.
        self.arbol.registrar_contagio(quien_contagio.nombre, persona.nombre)

    def aumentar_defensa_cada_x_turnos(self) -> None:
        """Cada cierto número de rondas, las personas sanas recuperan defensa."""
        # Verifica si se cumple el intervalo de bonus.
        if self.ronda > 0 and self.ronda % self.BONUS_INTERVALO == 0:
            # Recorre todas las personas.
            for persona in self.personas:
                # Solo aplica el bonus a las personas sanas.
                if not persona.infectado:
                    # Aumenta su defensa sin pasar el máximo permitido.
                    persona.defensa = min(persona.defensa + self.BONUS_INC, persona.defensa_max)

    # ---------------------------------------------------
    #*              ACCIONES EXTERNAS
    # ---------------------------------------------------
    def curar_persona(self, nombre: str) -> None:
        """Permite curar manualmente a una persona infectada."""
        # Recorre todas las personas para encontrar la que tiene ese nombre.
        for persona in self.personas:
            if persona.nombre == nombre:
                # Si está infectada, la cura.
                if persona.infectado:
                    persona.infectado = False
                    # Restaura su defensa base.
                    persona.defensa = self.DEF_BASE
                    # Elimina su registro del árbol de contagio.
                    self.arbol.eliminar_persona(nombre)
                    print(nombre, "ha sido curado.")
                    return
                else:
                    # Si no está infectado, se avisa.
                    print(nombre, "no está infectado.")
                    return
        # Si no se encuentra a nadie con ese nombre, se muestra un mensaje.
        print("No existe una persona con ese nombre.")

    def agregar_persona(self, nombre: str, x: int, y: int) -> None:
        """Agrega una nueva persona manualmente al mapa."""
        # Crea una nueva persona con los parámetros dados.
        nueva = Persona(nombre, x, y, self.DEF_BASE, self.DEF_MAX)
        # La agrega a la lista general de personas.
        self.personas.append(nueva)
        print("Persona agregada:", nombre)

    # ---------------------------------------------------
    #*                 MOSTRAR ESTADO
    # ---------------------------------------------------
    def mostrar_estado(self) -> None:
        """Muestra las personas infectadas, sanas y el árbol de contagios."""
        print("\n--- ESTADO DEL MAPA ---")

        print("\nPersonas infectadas:")
        # Recorre todas las personas y muestra las que están infectadas.
        for p in self.personas:
            if p.infectado:
                print(" ", p.nombre)
    
        # Muestra el árbol completo de contagios.
        self.arbol.mostrar_arbol()

        # Muestra las personas sanas con su defensa actual.
        print("Personas sanas:")
        for p in self.personas:
            if not p.infectado:
                print(" ", p.nombre, "defensa:", p.defensa)

    # ---------------------------------------------------
    #*                 EJECUTAR UNA RONDA
    # ---------------------------------------------------
    def ejecutar_ronda(self) -> None:
        """Ejecuta una ronda completa: movimiento, contagio, bonus y visualización."""
        # Aumenta el contador de rondas.
        self.ronda += 1
        print("\n===== RONDA", self.ronda, "=====")

        # Mueve todas las personas.
        self.mover_todas_las_personas()

        # Revisa posibles contagios después del movimiento.
        self.revisar_contagios()

        # Aplica el aumento de defensa si corresponde.
        self.aumentar_defensa_cada_x_turnos()

        # Muestra el estado general de la simulación.
        self.mostrar_estado()

        # Dibuja el mapa actual con las posiciones.
        self.mapa.imprimir_mapa(self.personas)