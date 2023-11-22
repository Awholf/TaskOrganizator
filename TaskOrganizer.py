import networkx as nx
import matplotlib.pyplot as plt
import random
import mplcursors
from matplotlib.widgets import Button
import numpy as np
import itertools


print(f"    _______        _       ____                        _")
print(f"   |__   __|      | |     / __ \                      (_)")
print(f"      | | __ _ ___| | __ | |  | |_ __ __ _  __ _ _ __  _ _______ _ __")
print(f"      | |/ _` / __| |/ / | |  | | '__/ _` |/ _` | '_ \| |_  / _ \ '__|")
print(f"      | | (_| \__ \   <  | |__| | | | (_| | (_| | | | | |/ /  __/ |")
print(f"      |_|\__,_|___/_|\_\  \____/|_|  \__, |\__,_|_| |_|_/___\___|_|")
print(f"                                      __/ |")
print(f"                                     |___/    ")


def obtener_numero_cursos():
    while True:
        try:
            num_cursos = int(input("Ingresa el número total de cursos que estás llevando: "))
            if num_cursos <= 0:
                print("Ingresa un número válido mayor que cero.")
            else:
                return num_cursos
        except ValueError:
            print("Ingresa un número válido.")

cant_arb = int(input("Ingresa la cantidad de formas en las que te gustaría organizar tu forma de estudio: "))

#Número de cursos
num_cursos = obtener_numero_cursos()
nombres_curso = []
for i in range(num_cursos):
    nombre_curso = input(f"Ingrese el nombre del curso {i + 1}: ")
    nombres_curso.append(nombre_curso)


def generar_arbol():
    #Crea grafo dirigido
    G = nx.DiGraph()

    nodo_inicio = "Inicio"
    nodo_fin = "Fin"
    G.add_node(nodo_inicio)
    G.add_node(nodo_fin)

    nodos_cursos = [curso for curso in nombres_curso]
    for nodo in nodos_cursos:
        G.add_edge(nodo_inicio, nodo)

    #Conexión de nodos de manera aleatoria
    random.shuffle(nodos_cursos)
    for i in range(len(nodos_cursos) - 1):
        G.add_edge(nodos_cursos[i], nodos_cursos[i + 1])

    nodo_final = nodos_cursos[-1]
    G.add_edge(nodo_final, nodo_fin)

    return G

# Crea el numero de organiaciones dadas por el usuario
num_arboles = cant_arb
fig, ax = plt.subplots(figsize=(5, 5))

graficos = []
for i in range(num_arboles):
    random.seed(i)
    G = generar_arbol()
    pos = nx.spring_layout(G, seed=42)
    graficos.append((G, pos))

#Itera entre los gráficos

iter_graficos = itertools.cycle(graficos)
current_index = 0

G, pos = next(iter_graficos)
nx.draw(
    G,
    pos,
    with_labels=True,
    node_size=3000,
    node_color="skyblue",
    font_weight="bold",
    arrows=True,
    ax=ax
)
ax.set_axis_off()

cursor = mplcursors.cursor(hover=False)

# Función para recorrer entre las organizaciones
def actualizar_grafico(ind):

    global current_index
    ax.clear()

    if ind == 1:
        G, pos = next(iter_graficos)
        current_index = (current_index + 1) % num_arboles
    elif ind == -1:
        G, pos = next(prev)
        current_index = (current_index - 1) % num_arboles

    nx.draw(
        G,
        pos,
        with_labels=True,
        node_size=4000,
        node_color="skyblue",
        font_weight="bold",
        arrows=True,
        ax=ax
    )

    ax.set_title(f"Organización #{current_index + 1}")
    cursor = mplcursors.cursor(hover=False)
    @cursor.connect("add")
    def on_add(sel):
        sel.artist.set_color("gray")
        fig.canvas.draw_idle()
        ax.axis('off')

    plt.draw()

# Configuración de botones para recorrer las organizaciones
prev = itertools.cycle(reversed(graficos))
axprev = plt.axes([0.05, 0.05, 0.1, 0.075])
axnext = plt.axes([0.16, 0.05, 0.1, 0.075])
bnext = Button(axnext, 'Siguiente')
bnext.on_clicked(lambda event: actualizar_grafico(1))
bprev = Button(axprev, 'Anterior')
bprev.on_clicked(lambda event: actualizar_grafico(-1))

ax.axis('off')
plt.show()