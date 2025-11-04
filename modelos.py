import random

# ---------------------------------------------------
#             CLASE PERSONA (UNA PERSONA EN EL MAPA)
# ---------------------------------------------------
class Persona:
    def __init__(self, nombre, pos_x, pos_y):
        # Información básica
        self.nombre = nombre
        self.x = pos_x
        self.y = pos_y
        
        # Salud
        self.defensa = 3       # puntos de defensa
        self.infectado = False # estado de infección

    # ----- Movimiento -----
    def mover_una_celda(self, tamaño_mapa):
        # Movimiento aleatorio -1, 0 o 1
        mover_x = random.randint(-1, 1)
        mover_y = random.randint(-1, 1)

        # Nuevo intento de posición
        nueva_x = self.x + mover_x
        nueva_y = self.y + mover_y

        # Corregir si sale del mapa
        nueva_x = self.ajustar_posicion(nueva_x, tamaño_mapa)
        nueva_y = self.ajustar_posicion(nueva_y, tamaño_mapa)

        # Actualizar posición
        self.x = nueva_x
        self.y = nueva_y

    def ajustar_posicion(self, valor, limite):
        if valor < 0:
            return 0
        if valor >= limite:
            return limite - 1
        return valor


# ---------------------------------------------------
#         CLASE ARBOL DE CONTAGIO (QUIÉN INFECTÓ A QUIÉN)
# ---------------------------------------------------
class ArbolContagio:
    def __init__(self):
        self.registros = {}

    def registrar_contagio(self, infectador, infectado):
        if infectador not in self.registros:
            self.registros[infectador] = []
        self.registros[infectador].append(infectado)

    def eliminar_persona(self, persona):
        # quitar de todas las listas
        for clave in self.registros:
            if persona in self.registros[clave]:
                self.registros[clave].remove(persona)

        # borrar si tenía su propia lista
        if persona in self.registros:
            del self.registros[persona]

    def mostrar_arbol(self):
        print("\nÁrbol de contagio:")
        if not self.registros:
            print("  No hay contagios aún.")
        else:
            for persona in self.registros:
                print(" ", persona, "infectó a:", self.registros[persona])


# ---------------------------------------------------
#                 CLASE MATRIZ (EL MAPA)
# ---------------------------------------------------
class Matriz:
    def __init__(self, tamaño):
        self.tamaño = tamaño

    def imprimir_mapa(self, lista_personas):
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

    def buscar_personas_celda(self, lista, x, y):
        resultado = []
        for p in lista:
            if p.x == x and p.y == y:
                resultado.append(p)
        return resultado
import random

# ---------------------------------------------------
#                 SIMULACIÓN GENERAL
# ---------------------------------------------------
class Simulacion:
    def __init__(self, tamaño_mapa, cantidad_personas):
        # Tamaño del mapa (por ejemplo 10x10)
        self.tamaño = tamaño_mapa

        # Lista que guardará todas las personas
        self.personas = []

        # Contador de rondas
        self.ronda = 0

        # Árbol que guarda quién contagió a quién
        self.arbol = ArbolContagio()

        # Crear el mapa
        self.mapa = Matriz(tamaño_mapa)

        # Crear personas y elegir paciente cero
        self.crear_personas_iniciales(cantidad_personas)
        self.elegir_paciente_cero()

    # ---------------------------------------------------
    #              CREAR Y CONFIGURAR PERSONAS
    # ---------------------------------------------------
    def crear_personas_iniciales(self, cantidad):
        """Crea las personas con posiciones aleatorias."""
        for i in range(cantidad):
            nombre = "p" + str(i + 1)
            x = random.randint(0, self.tamaño - 1)
            y = random.randint(0, self.tamaño - 1)
            nueva_persona = Persona(nombre, x, y)
            self.personas.append(nueva_persona)

    def elegir_paciente_cero(self):
        """Elige una persona al azar para comenzar infectada."""
        paciente = random.choice(self.personas)
        paciente.infectado = True
        self.arbol.registros[paciente.nombre] = []

    # ---------------------------------------------------
    #                   LÓGICA DEL JUEGO
    # ---------------------------------------------------
    def mover_todas_las_personas(self):
        """Hace que todas las personas se muevan una celda."""
        for persona in self.personas:
            persona.mover_una_celda(self.tamaño)

    def revisar_contagios(self):
        """Verifica si hay contagios entre personas en la misma celda."""
        for persona in self.personas:
            if persona.infectado == False:
                infectados = self.buscar_infectados_en_misma_celda(persona)

                # Si hay infectados, baja la defensa
                if len(infectados) > 0:
                    persona.defensa -= len(infectados)

                    # Si la defensa llega a 0, se contagia
                    if persona.defensa <= 0:
                        self.infectar_persona(persona, infectados)

    def buscar_infectados_en_misma_celda(self, persona):
        """Devuelve una lista de infectados que están en la misma posición."""
        infectados = []
        for otro in self.personas:
            if otro.x == persona.x and otro.y == persona.y and otro.infectado:
                infectados.append(otro)
        return infectados

    def infectar_persona(self, persona, infectadores):
        """Marca a una persona como infectada y registra quién la contagió."""
        persona.infectado = True
        quien_contagio = random.choice(infectadores)
        self.arbol.registrar_contagio(quien_contagio.nombre, persona.nombre)

    def aumentar_defensa_cada_3_turnos(self):
        """Cada 3 rondas, los sanos ganan un punto de defensa."""
        if self.ronda % 3 == 0 and self.ronda > 0:
            for persona in self.personas:
                if persona.infectado == False:
                    persona.defensa += 1

    # ---------------------------------------------------
    #                    ACCIONES EXTERNAS
    # ---------------------------------------------------
    def curar_persona(self, nombre):
        """Cura a una persona infectada."""
        for persona in self.personas:
            if persona.nombre == nombre:
                if persona.infectado:
                    persona.infectado = False
                    persona.defensa = 3
                    self.arbol.eliminar_persona(nombre)
                    print(nombre, "ha sido curado.")
                    return
                else:
                    print(nombre, "no está infectado.")
                    return
        print("No existe una persona con ese nombre.")

    def agregar_persona(self, nombre, x, y):
        """Agrega una nueva persona en la posición dada."""
        nueva = Persona(nombre, x, y)
        self.personas.append(nueva)
        print("Persona agregada:", nombre)

    # ---------------------------------------------------
    #                    MOSTRAR ESTADO
    # ---------------------------------------------------
    def mostrar_estado(self):
        """Muestra las personas sanas e infectadas."""
        print("\n--- ESTADO DEL MAPA ---")

        print("Personas sanas:")
        for p in self.personas:
            if not p.infectado:
                print(" ", p.nombre, "defensa:", p.defensa)

        print("\nPersonas infectadas:")
        for p in self.personas:
            if p.infectado:
                print(" ", p.nombre)

        # Mostrar árbol de contagio
        self.arbol.mostrar_arbol()

    # ---------------------------------------------------
    #                EJECUTAR UNA RONDA
    # ---------------------------------------------------
    def ejecutar_ronda(self):
        """Ejecuta los pasos de una ronda completa."""
        self.ronda += 1
        print("\n===== RONDA", self.ronda, "=====")

        # 1. Mover personas
        self.mover_todas_las_personas()

        # 2. Revisar contagios
        self.revisar_contagios()

        # 3. Subir defensa si corresponde
        self.aumentar_defensa_cada_3_turnos()

        # 4. Mostrar el mapa y el estado
        self.mapa.imprimir_mapa(self.personas)
        self.mostrar_estado()
