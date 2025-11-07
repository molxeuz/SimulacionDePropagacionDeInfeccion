
import random
from typing import Dict, List, Set

random.seed(123)

# ---------------------------------------------------
#*                     CLASE PERSONA (UNA PERSONA EN EL MAPA)
# ---------------------------------------------------
class Persona:
    """Representa una persona en el mapa con posición y estado de salud."""

    def __init__(self, nombre: str, pos_x: int, pos_y: int, defensa_base: int, defensa_max: int) -> None:
        self.nombre = nombre
        self.x = pos_x
        self.y = pos_y

        self.defensa: int = defensa_base     
        self.defensa_max: int = defensa_max    
        self.infectado: bool = False          

    #? ----- Movimiento -----

    def mover_una_celda(self, tamaño_mapa: int, lista_personas: List["Persona"]) -> None:
        """Mueve a la persona aleatoriamente, pero no a una celda ocupada por otra persona sana."""
        
        for _ in range(10):  # intenta 10 veces encontrar un lugar donde se oueda mover
            mover_x = random.randint(-1, 1)
            mover_y = random.randint(-1, 1)
            nueva_x = self.ajustar_posicion(self.x + mover_x, tamaño_mapa)
            nueva_y = self.ajustar_posicion(self.y + mover_y, tamaño_mapa)

            if (nueva_x, nueva_y) == (self.x, self.y):
                return 

            # Verifica si hay otra persona sana a donde se va a mover
            ocupado = False
            for p in lista_personas:
                if p.x == nueva_x and p.y == nueva_y and not p.infectado and p != self:
                    ocupado = True
                    break
            if not ocupado:
                self.x = nueva_x
                self.y = nueva_y
                return

    def ajustar_posicion(self, valor: int, limite: int) -> int:
        """Ajusta un valor de coordenada para que permanezca dentro del mapa."""
        if valor < 0:
            return 0
        if valor >= limite:
            return limite - 1
        return valor

# ---------------------------------------------------
#*         CLASE ARBOL DE CONTAGIO (QUIÉN INFECTÓ A QUIÉN)
# ---------------------------------------------------
class ArbolContagio:
    """Arbol donde se registra quién contagió a quién."""

    def __init__(self) -> None:
        self.registros: Dict[str, List[str]] = {}

    def registrar_contagio(self, infectador: str, infectado: str) -> None:
        if infectador not in self.registros:
            self.registros[infectador] = []
        self.registros[infectador].append(infectado)

    def eliminar_persona(self, persona: str) -> None:
        """Elimina una persona del árbol de contagio."""

        # quitar de todas las listas
        for clave in list(self.registros.keys()):
            if persona in self.registros[clave]:
                self.registros[clave].remove(persona)

        # borrar si tenía su propia lista
        if persona in self.registros:
            del self.registros[persona]

    def mostrar_arbol(self) -> None:
        """Imprime el/los árbol(es) de contagio en ASCII y muestra la traza más larga."""
        print("\nÁrbol de contagio:")
        if not self.registros:
            print("  No hay contagios aún.")
            return

        # calcular raíces: claves que nunca aparecen como hijos
        infectados = {h for hijos in self.registros.values() for h in hijos}
        raices = set(self.registros.keys()) - infectados
        if not raices:
            raices = set(self.registros.keys())
        raices_ordenadas = sorted(raices)

        # ---------- funciones internas ----------
        def imprimir_subarbol(nodo: str, pref: str, visitados: set) -> None:
            """Imprime recursivamente los hijos con conectores ASCII."""
            if nodo in visitados:
                print(pref + "└── (ciclo detectado)")
                return
            visitados.add(nodo)
            hijos = sorted(self.registros.get(nodo, []))
            for i, h in enumerate(hijos):
                es_ultimo = (i == len(hijos) - 1)
                con = "└── " if es_ultimo else "├── "
                print(pref + con + h)
                siguiente_pref = pref + ("    " if es_ultimo else "│   ")
                imprimir_subarbol(h, siguiente_pref, visitados.copy())

        def camino_mas_largo_desde(nodo: str, visitados: set) -> list:
            """
            Devuelve lista con el camino más largo desde 'nodo'.
            Evita ciclos usando 'visitados'.
            """
            if nodo in visitados:
                return [nodo]
            visitados = visitados | {nodo}
            mejor = [nodo]
            for h in sorted(self.registros.get(nodo, [])):
                camino = camino_mas_largo_desde(h, visitados)
                if len(camino) + 1 > len(mejor):
                    mejor = [nodo] + camino
            return mejor
        # ----------------------------------------

        # imprimir cada raíz y su subárbol
        for i, raiz in enumerate(raices_ordenadas):
            es_ultima_raiz = (i == len(raices_ordenadas) - 1)
            conector = "└── " if es_ultima_raiz else "├── "
            print(conector + raiz)
            pref = "    " if es_ultima_raiz else "│   "
            imprimir_subarbol(raiz, pref, set())

        # calcular traza más larga entre todas las raíces y mostrarla
        mejor_total = []
        for raiz in raices_ordenadas:
            camino = camino_mas_largo_desde(raiz, set())
            if len(camino) > len(mejor_total):
                mejor_total = camino

        if mejor_total:
            print("\nTraza más larga del contagio:")
            print(" → ".join(mejor_total))
        else:
            print("\nNo se encontró traza más larga.")

# ---------------------------------------------------
#*                 CLASE MATRIZ 
# ---------------------------------------------------
class Matriz:
    """Mapa cuadrado de tamaño fijo donde se mueven las personas."""

    def __init__(self, tamaño: int) -> None:
        self.tamaño: int = tamaño

    def imprimir_mapa(self, lista_personas: List[Persona]) -> None:
        print("\nMapa:")

        # Recorrer cada celda
        for fila in range(self.tamaño):
            linea = ""
            for col in range(self.tamaño):
                personas_en_celda = self.buscar_personas_celda(lista_personas, fila, col)

                if len(personas_en_celda) == 0:
                    linea += "⬜ "
                elif len(personas_en_celda) > 1:
                    linea += "⚠️ "
                else:
                    persona = personas_en_celda[0]
                    if persona.infectado:
                        linea += "🟥 "
                    else:
                        linea += "🟩 "
            print(linea)

    def buscar_personas_celda(self, lista: List[Persona], x: int, y: int) -> List[Persona]:
        """Devuelve la lista de personas que ocupan la celda (x, y)."""
        resultado: List[Persona] = []
        for p in lista:
            if p.x == x and p.y == y:
                resultado.append(p)
        return resultado

# ---------------------------------------------------
#*                 SIMULACIÓN GENERAL
# ---------------------------------------------------
class Simulacion:
    """Orquesta el ciclo de rondas, movimiento, contagios y visualización."""

    def __init__(self, tamaño_mapa: int, cantidad_personas: int) -> None:
        self.tamaño: int = tamaño_mapa
        self.personas: List[Persona] = []
        self.sanos: List[Persona] = []
        self.infectados: List[Persona] = []
        self.ronda: int = 0
        self.arbol: ArbolContagio = ArbolContagio()
        self.mapa: Matriz = Matriz(tamaño_mapa)

        if self.tamaño >= 5: 
            self.DEF_BASE = 1
            self.DEF_MAX = 2
        else:
            self.DEF_BASE = max(1, self.tamaño // 2)                  # defensa inicial
            self.DEF_MAX  = max(self.DEF_BASE, (self.tamaño // 2) + 1)      # max e de defensa
        
        self.crear_personas_iniciales(cantidad_personas)
        self.elegir_paciente_cero()
        self.BONUS_INTERVALO = max(6, ((self.tamaño // 2) + 1))            # cada cuántas rondas hay bonus
        self.BONUS_INC = 1

    # ---------------------------------------------------
    #*              CREAR Y CONFIGURAR PERSONAS
    # ---------------------------------------------------
    def crear_personas_iniciales(self, cantidad: int) -> None:
        """Crea las personas con posiciones aleatorias dentro del mapa."""

        for i in range(cantidad):
            nombre = f"p{i + 1}"
            x = random.randint(0, self.tamaño - 1)
            y = random.randint(0, self.tamaño - 1)
            nueva_persona = Persona(nombre, x, y, defensa_base=self.DEF_BASE, defensa_max=self.DEF_MAX)
            self.personas.append(nueva_persona)
            self.sanos.append(nueva_persona)

    def elegir_paciente_cero(self) -> None:
        """Elige una persona al azar para comenzar infectada."""

        paciente = random.choice(self.personas)
        paciente.infectado = True
        self.infectados.append(paciente) 
        self.sanos.remove(paciente)
        self.arbol.registros[paciente.nombre] = []

    # ---------------------------------------------------
    #*                   LÓGICA DEL JUEGO
    # ---------------------------------------------------
    def mover_todas_las_personas(self) -> None:
        """Hace que todas las personas se muevan una celda."""

        for persona in self.personas:
            persona.mover_una_celda(self.tamaño, lista_personas=self.personas)

    def revisar_contagios(self) -> None:
        """Verifica si hay contagios entre personas en la misma celda."""

        for persona in list(self.sanos):
            if persona.infectado is False:
                infectados = self.buscar_infectados_en_misma_celda(persona)

                # Si hay infectados en la misma celda le quita defensa
                if len(infectados) > 0:
                    persona.defensa -= len(infectados)

                    # Si la defensa llega a 0 se contagia
                    if persona.defensa <= 0:
                        self.infectar_persona(persona, infectados)

    def buscar_infectados_en_misma_celda(self, persona: Persona) -> List[Persona]:
        """Devuelve una lista de infectados que están en la misma posición."""

        infectados = []
        for otro in self.infectados:
            if otro.x == persona.x and otro.y == persona.y:
                infectados.append(otro)
        return infectados

    def infectar_persona(self, persona: Persona, infectadores: List[Persona]) -> None:
        """Marca a una persona como infectada y registra quién la contagió."""

        if persona in self.sanos:
            self.sanos.remove(persona)

        if persona not in self.infectados:
            self.infectados.append(persona)

        persona.infectado = True
        quien_contagio = random.choice(infectadores)
        self.arbol.registrar_contagio(quien_contagio.nombre, persona.nombre)

    def aumentar_defensa_cada_x_turnos(self) -> None:
        """Cada x rondas los sanos ganan defensa."""

        if self.ronda > 0 and self.ronda % self.BONUS_INTERVALO == 0:
            for persona in self.sanos:
                persona.defensa = min(persona.defensa + self.BONUS_INC, persona.defensa_max)

    # ---------------------------------------------------
    #*                    ACCIONES EXTERNAS
    # ---------------------------------------------------

    def curar_persona(self, x: int, y: int) -> None:
        """Cura a una persona infectada."""

        for persona in self.personas:
            if persona.x == x and persona.y == y:
                if persona.infectado:
                    persona.infectado = False
                    persona.defensa = self.DEF_BASE
                    self.arbol.eliminar_persona(persona.nombre)

                    if persona in self.infectados:
                        self.infectados.remove(persona)
                    if persona not in self.sanos:
                        self.sanos.append(persona)

                    print(persona.nombre, "ha sido curado.")
                    return
                else:
                    print(persona.nombre, "no está infectado.")
                    return
        print("No existe una persona en esa posición.")


    def agregar_persona(self, nombre: str, x: int, y: int) -> None:
        """Agrega una nueva persona en la posición dada."""

        nueva = Persona(nombre, x, y, self.DEF_BASE, self.DEF_MAX)
        self.personas.append(nueva)
        self.sanos.append(nueva)
        print("Persona agregada:", nombre)

    # ---------------------------------------------------
    #*                    MOSTRAR ESTADO
    # ---------------------------------------------------
    def mostrar_estado(self) -> None:
        """Muestra las personas sanas e infectadas."""

        print("\n--- ESTADO DEL MAPA ---")

        print("\nPersonas infectadas:")
        for p in self.infectados:  
            print(" ", p.nombre)
    
        self.arbol.mostrar_arbol()

        print("Personas sanas:")
        for p in self.sanos:       
            print(" ", p.nombre, "defensa:", p.defensa)

    # ---------------------------------------------------
    #*                EJECUTAR UNA RONDA
    # ---------------------------------------------------
    def ejecutar_ronda(self) -> None:
        """Ejecuta los pasos de una ronda completa."""
        
        self.ronda += 1
        print("\n===== RONDA", self.ronda, "=====")

        self.mover_todas_las_personas()
        self.revisar_contagios()
        self.aumentar_defensa_cada_x_turnos()

        self.mostrar_estado()
        self.mapa.imprimir_mapa(self.personas)