import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import tkinter as tk
from tkinter import ttk
import threading

# Función para trazar puntos en los octantes del círculo
def trazar_puntos_circulo(Xc, Yc, x, y, octantes):
    octantes[0].append((Xc + x, Yc + y))
    octantes[1].append((Xc - x, Yc + y))
    octantes[2].append((Xc + x, Yc - y))
    octantes[3].append((Xc - x, Yc - y))
    octantes[4].append((Xc + y, Yc + x))
    octantes[5].append((Xc - y, Yc + x))
    octantes[6].append((Xc + y, Yc - x))
    octantes[7].append((Xc - y, Yc - x))

# Algoritmo del punto medio para dibujar un círculo
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

    # Añadir puntos adicionales para mejorar la precisión
    puntos_finos = []
    for (x, y, p) in puntos:
        puntos_finos.append((x, y, p))
        puntos_finos.append((x + 0.5, y, p))
        puntos_finos.append((x, y + 0.5, p))
        puntos_finos.append((x + 0.5, y + 0.5, p))
        
    return puntos_finos, octantes

# Algoritmo DDA para dibujar una línea
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

# Función para rellenar el círculo
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

# Función para imprimir las tablas de puntos calculados
def imprimir_tablas(puntos, Xc, Yc):
    root = tk.Tk()
    root.title("Tablas de Puntos Calculados")

    # Obtener el ancho y alto de la pantalla
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Establecer el tamaño y posición de la ventana
    window_width = screen_width // 2
    window_height = screen_height // 2
    root.geometry(f"{window_width}x{window_height}+{screen_width - window_width}+0")

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

# Función para graficar el círculo de manera animada
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

    plt.figtext(0.5, 0.98, 'Hecho por Jared Salazar', ha='center', fontsize=8)
    plt.figtext(0.5, 0.95, f'Centro: ({Xc}, {Yc})  Radio: {r}', ha='center', fontsize=12)

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

    # Mostrar la gráfica
    plt.show()

# Función para solicitar los parámetros del círculo al usuario
def solicitar_parametros():
    def obtener_parametros():
        Xc = entry_Xc.get()
        Yc = entry_Yc.get()
        r = entry_r.get()
        
        # Verificamos si los valores son válidos
        try:
            Xc, Yc, r = int(Xc), int(Yc), int(r)
            print(f"Centro: ({Xc}, {Yc}), Radio: {r}")
            
            # Llamar al algoritmo principal con los parámetros
            puntos, octantes = algoritmo_punto_medio_circulo(Xc, Yc, r)
            puntos_borde = set()
            for octante in octantes:
                puntos_borde.update(octante)
            puntos_relleno = rellenar_circulo(puntos_borde, Xc, Yc)

            # Ejecutar funciones en paralelo
            hilo_tablas = threading.Thread(target=imprimir_tablas, args=(puntos, Xc, Yc))
            hilo_animacion = threading.Thread(target=graficar_circulo_animado, args=(puntos_relleno, puntos_borde, Xc, Yc, r))

            hilo_tablas.start()
            hilo_animacion.start()

        except ValueError:
            print("Por favor, introduce valores numéricos válidos.")
        
        # Limpiar los campos de entrada para nuevos valores
        entry_Xc.delete(0, tk.END)
        entry_Yc.delete(0, tk.END)
        entry_r.delete(0, tk.END)

    def focus_next_widget(event):
        event.widget.tk_focusNext().focus()
        return "break"

    root = tk.Tk()
    root.title("Parámetros del Círculo")

    # Centrar la ventana de entrada en la pantalla
    window_width = 300
    window_height = 150
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    position_top = int(screen_height / 2 - window_height / 2)
    position_right = int(screen_width / 2 - window_width / 2)
    root.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")

    tk.Label(root, text="Coordenada X del centro:").grid(row=0, column=0)
    entry_Xc = tk.Entry(root)
    entry_Xc.grid(row=0, column=1)
    entry_Xc.bind("<Return>", focus_next_widget)

    tk.Label(root, text="Coordenada Y del centro:").grid(row=1, column=0)
    entry_Yc = tk.Entry(root)
    entry_Yc.grid(row=1, column=1)
    entry_Yc.bind("<Return>", focus_next_widget)

    tk.Label(root, text="Radio:").grid(row=2, column=0)
    entry_r = tk.Entry(root)
    entry_r.grid(row=2, column=1)
    entry_r.bind("<Return>", focus_next_widget)

    tk.Button(root, text="Aceptar", command=obtener_parametros).grid(row=3, columnspan=2)

    root.mainloop()

# Función principal
def main():
    # Solicitar al usuario los parámetros del círculo
    solicitar_parametros()

if __name__ == "__main__":
    main()