import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import tkinter as tk
from tkinter import ttk
import threading

def trazar_puntos_circulo(Xc, Yc, x, y, octantes):
    octantes[0].append((Xc + x, Yc + y))
    octantes[1].append((Xc - x, Yc + y))
    octantes[2].append((Xc + x, Yc - y))
    octantes[3].append((Xc - x, Yc - y))
    octantes[4].append((Xc + y, Yc + x))
    octantes[5].append((Xc - y, Yc + x))
    octantes[6].append((Xc + y, Yc - x))
    octantes[7].append((Xc - y, Yc - x))

def algoritmo_punto_medio_circulo(Xc, Yc, r):
    x = 0
    y = r
    p = 1 - r
    puntos = [(x, y, p)]
    octantes = [[] for _ in range(8)]

    trazar_puntos_circulo(Xc, Yc, x, y, octantes)

    while x < y:
        x += 1
        if p < 0:
            p = p + 2 * x + 1
        else:
            y -= 1
            p = p + 2 * x + 1 - 2 * y
        puntos.append((x, y, p))
        trazar_puntos_circulo(Xc, Yc, x, y, octantes)

    return puntos, octantes

def linea_dda(x0, y0, x1, y1):
    puntos = []
    dx = x1 - x0
    dy = y1 - y0
    pasos = max(abs(dx), abs(dy))
    incremento_x = dx / pasos
    incremento_y = dy / pasos
    x = x0
    y = y0
    for _ in range(pasos + 1):
        puntos.append((round(x), round(y)))
        x += incremento_x
        y += incremento_y
    return puntos

def rellenar_circulo(puntos_borde, Xc, Yc):
    puntos_relleno = set(puntos_borde)
    y_min = min(p[1] for p in puntos_borde)
    y_max = max(p[1] for p in puntos_borde)

    for y in range(y_min, y_max + 1):
        puntos_en_y = [p for p in puntos_borde if p[1] == y]
        if len(puntos_en_y) > 1:
            x_min = min(p[0] for p in puntos_en_y)
            x_max = max(p[0] for p in puntos_en_y)
            puntos_relleno.update(linea_dda(x_min, y, x_max, y))

    return puntos_relleno

def imprimir_tablas(puntos, Xc, Yc):
    root = tk.Tk()
    root.title("Tablas de Puntos Calculados")

    tab_control = ttk.Notebook(root)

    tabs = []
    nombres_octantes = ["N Pk Xk+1 Yk-1", "Y X", "X -Y", "-Y X", "-Y -X", "-X -Y", "-X Y", "Y -X"]
    for i in range(8):
        tab = ttk.Frame(tab_control)
        tab_control.add(tab, text=nombres_octantes[i])
        tabs.append(tab)

    tab_control.pack(expand=1, fill='both')

    for i, tab in enumerate(tabs):
        if i == 0:
            headers = ["N", "Pk", "Xk+1", "Yk-1"]
        else:
            headers = ["Xk+1", "Yk-1"]
        
        tree = ttk.Treeview(tab, columns=headers, show='headings')
        for header in headers:
            tree.heading(header, text=header)
            tree.column(header, anchor='center')
        tree.pack(expand=1, fill='both')

        for j, (x, y, p) in enumerate(puntos):
            if i == 0:
                if j == 0:
                    tree.insert("", "end", values=(j, p, x + 1, y))
                else:
                    if puntos[j-1][2] < 0:
                        tree.insert("", "end", values=(j, p, x + 1, y))
                    else:
                        tree.insert("", "end", values=(j, p, x + 1, y - 1))
            elif i == 1:
                tree.insert("", "end", values=(y, x))
            elif i == 2:
                tree.insert("", "end", values=(x, -y))
            elif i == 3:
                tree.insert("", "end", values=(-y, x))
            elif i == 4:
                tree.insert("", "end", values=(-y, -x))
            elif i == 5:
                tree.insert("", "end", values=(-x, -y))
            elif i == 6:
                tree.insert("", "end", values=(-x, y))
            elif i == 7:
                tree.insert("", "end", values=(y, -x))

    root.mainloop()

def graficar_circulo_animado(puntos_relleno, puntos_borde, Xc, Yc, r):
    fig, ax = plt.subplots()
    ax.set_aspect('equal', adjustable='box')
    ax.grid(True)
    ax.set_xlim(Xc - r - 1, Xc + r + 1)
    ax.set_ylim(Yc - r - 1, Yc + r + 1)

    x_vals_relleno = [p[0] for p in puntos_relleno]
    y_vals_relleno = [p[1] for p in puntos_relleno]

    x_vals_borde = [p[0] for p in puntos_borde]
    y_vals_borde = [p[1] for p in puntos_borde]

    relleno = ax.scatter([], [], color='r')
    borde = ax.scatter([], [], color='b')

    def init():
        relleno.set_offsets(np.empty((0, 2)))
        borde.set_offsets(np.empty((0, 2)))
        return relleno, borde

    def animate(i):
        relleno.set_offsets(np.c_[x_vals_relleno[:i], y_vals_relleno[:i]])
        borde.set_offsets(np.c_[x_vals_borde[:i], y_vals_borde[:i]])
        if i == len(x_vals_relleno) - 1:
            ani.event_source.stop()
        return relleno, borde

    ani = animation.FuncAnimation(fig, animate, init_func=init, frames=len(x_vals_relleno), interval=50, blit=True)
    plt.show()

def main():
    # Solicitar al usuario los parámetros del círculo
    Xc = int(input("Ingrese la coordenada X del centro del círculo: "))
    Yc = int(input("Ingrese la coordenada Y del centro del círculo: "))
    r = int(input("Ingrese el radio del círculo: "))

    # Obtener los puntos del círculo y los octantes
    puntos, octantes = algoritmo_punto_medio_circulo(Xc, Yc, r)

    # Obtener los puntos del borde del círculo
    puntos_borde = set()
    for octante in octantes:
        puntos_borde.update(octante)

    # Rellenar el círculo
    puntos_relleno = rellenar_circulo(puntos_borde, Xc, Yc)

    # Crear hilos para ejecutar las funciones en paralelo
    hilo_tablas = threading.Thread(target=imprimir_tablas, args=(puntos, Xc, Yc))
    hilo_animacion = threading.Thread(target=graficar_circulo_animado, args=(puntos_relleno, puntos_borde, Xc, Yc, r))

    # Iniciar los hilos
    hilo_tablas.start()
    hilo_animacion.start()

    # Esperar a que los hilos terminen
    hilo_tablas.join()
    hilo_animacion.join()

if __name__ == "__main__":
    main()