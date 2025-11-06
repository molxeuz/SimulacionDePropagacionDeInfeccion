# Resident Evil UDEM  
### Simulación de propagación de infección en una matriz con árbol de contagio  
**Archivo principal:** `PracticaArbolesTaller.ipynb`  
**Desarrollado por:** `Mateo Molina Gonzalez & Manuel Gutierrez Villegas`  

---

## Contexto general

Esta práctica implementa una **simulación de propagación de una infección** dentro de una **matriz NxN**, donde `n` personas (`p1`, `p2`, …, `pn`) se mueven aleatoriamente en todas las direcciones.  

Al inicio, una persona es seleccionada aleatoriamente como **paciente cero** (infectada). Durante cada ronda:  
- Las personas se mueven aleatoriamente (8 direcciones posibles).  
- Si una persona **infectada** se cruza o comparte posición con una persona **sana**, la sana pierde 1 punto de defensa.  
- Cuando la defensa llega a **0**, la persona se **infecta automáticamente**.  

El sistema mantiene un **árbol de propagación de infección**, registrando quién contagió a quién.  
La simulación termina cuando el usuario lo decida o cuando **todas las personas estén infectadas**.

---

## Reglas y dinámica de la simulación

### Inicialización
- El usuario define el **tamaño de la matriz (N)** y el **número de personas (n)**.  
- Las personas se ubican **aleatoriamente** en la matriz (una por celda al inicio).  
- Una persona aleatoria es el **paciente cero (infectada)**.  
- Las demás inician **sanas** con un **nivel de defensa = 3** (parametrizable).

---

### Movimiento
- Cada ronda, todas las personas se mueven una celda adyacente aleatoria (N, S, E, O, y diagonales).  
- Si intentan salir de la matriz:
  - Opción A: rebotan y permanecen en la misma celda.  
  - Opción B: se desplazan circularmente (modo **toroide**).  
- El grupo debe **documentar qué opción utiliza**.

---

### Cruces e infección
- Si una persona **sana** comparte celda con una o más **infectadas**:
  - Pierde **1 punto de defensa por cada cruce**.  
  - Si su defensa llega a 0 → se **infecta**.  
- Se actualiza el **árbol de propagación** agregando una arista *(infectador → nuevo infectado)*.

---

### Curación
- El usuario puede ejecutar la acción `curar(x, y)` indicando coordenadas.  
- Si la persona está infectada:
  - Pasa a **sana** nuevamente.  
  - Se elimina del árbol de propagación.  
  - Sus descendientes pasan a ser **hijos directos** del infectador original.

---

### Agregar nuevas personas
- El usuario puede agregar nuevas personas (`pN+1`, `pN+2`, …) en coordenadas específicas.  
- Comienzan **sanas** con nivel de defensa **3**.

---

### Defensa especial
- Cada **3 rondas**, todas las personas **sanas** ganan **+1 defensa**.  
- Cada vez que una persona sana se cruza con una infectada, **pierde -1 defensa**.  
- Cuando su defensa llega a **0**, se **infecta automáticamente**.

---

## Visualización
Después de cada ronda, se muestra:

### Matriz
- Personas **sanas** en verde 🟩  
- Personas **infectadas** en rojo 🟥  
- Cada celda muestra el identificador (`p1`, `p2`, etc.)

### Estado general
- Listado de personas sanas con su **nivel de defensa**.  
- **Árbol de propagación** actualizado (formato ASCII o lista de adyacencia).

---

## Finalización
La simulación termina cuando:
- El usuario lo decida, **o**
- Todas las personas estén **infectadas**.

---

## Requisitos técnicos
- ✅ Uso **obligatorio de type hints** en todas las funciones y clases.  
- ✅ Implementación **orientada a objetos (POO)**.  
- ✅ Visualización: en consola o con interfaz gráfica simple.  
- ✅ **Código limpio**: separar lógica, datos y visualización.  
- ✅ Permitir **semilla (random.seed)** para reproducir experimentos idénticos.
