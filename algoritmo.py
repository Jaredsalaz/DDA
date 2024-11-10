import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import tkinter as tk
from tkinter import ttk
import threading

# Se progrmar en python pero nunca pude programar una cita con la chica que me gusta :(
# Se declarar funciones pero nuca pude declarar mi amor por ella :(

# Algoritmo del punto medio para dibujar un elipse
def algoritmo_punto_medio_elipse(Xc, Yc, Rx, Ry):
    puntos = []
    region1 = []
    region2 = []

    Rx2 = Rx * Rx
    Ry2 = Ry * Ry
    x = 0
    y = Ry

    # 1. Parámetro de decisión inicial para la Región 1
    # Fórmula: P1o = Ry^2 - Rx^2 * Ry + 0.25 * Rx^2
    p1 = Ry2 - (Rx2 * Ry) + (0.25 * Rx2)
    dx = 2 * Ry2 * x
    dy = 2 * Rx2 * y

    # Guardamos el primer punto con los valores iniciales
    trazar_puntos_elipse(Xc, Yc, x, y, puntos)
    region1.append((x, y, p1))

    # Región 1
    while dx < dy:
        if p1 < 0:
            # 2. Si Pk < 0, entonces (Xk+1, Yk)
            # Fórmula: P1k+1 = P1k + 2 * Ry^2 * Xk+1 + Ry^2
            x += 1
            dx += 2 * Ry2
            p1 += dx + Ry2
        else:
            # 3. Si Pk >= 0, entonces (Xk+1, Yk-1)
            # Fórmula: P1k+1 = P1k + 2 * Ry^2 * Xk+1 - 2 * Rx^2 * Yk+1 + Ry^2
            x += 1
            y -= 1
            dx += 2 * Ry2
            dy -= 2 * Rx2
            p1 += dx - dy + Ry2

        trazar_puntos_elipse(Xc, Yc, x, y, puntos)
        region1.append((x, y, p1))

    # Comprobación antes de pasar a la Región 2
    # Fórmula: Si 2 * Ry^2 * X >= 2 * Rx^2 * Y
    if 2 * Ry2 * x >= 2 * Rx2 * y:
        # 4. Parámetro de decisión inicial para la Región 2
        # Fórmula: P2o = Ry^2 * (Xo + 0.5)^2 + Rx^2 * (Yo - 1) ** 2 - Rx^2 * Ry^2
        p2 = Ry2 * (x + 0.5) ** 2 + Rx2 * (y - 1) ** 2 - Rx2 * Ry2

        # Región 2
        while y >= 0:
            if p2 > 0:
                # 5. Si P2k > 0, entonces (Xk, Yk-1)
                # Fórmula: P2k+1 = P2k - 2 * Rx^2 * Yk+1 + Rx^2
                y -= 1
                dy -= 2 * Rx2
                p2 += Rx2 - dy
            else:
                # 6. Si P2k <= 0, entonces (Xk+1, Yk-1)
                # Fórmula: P2k+1 = P2k + 2 * Ry^2 * Xk+1 - 2 * Rx^2 * Yk+1 + Rx^2
                x += 1
                y -= 1
                dx += 2 * Ry2
                dy -= 2 * Rx2
                p2 += dx - dy + Rx2

            trazar_puntos_elipse(Xc, Yc, x, y, puntos)
            region2.append((x, y, p2))

    return puntos, region1, region2

# Función para trazar puntos en los octantes de la elipse
def trazar_puntos_elipse(Xc, Yc, x, y, puntos):
    puntos.append((Xc + x, Yc + y))
    puntos.append((Xc - x, Yc + y))
    puntos.append((Xc + x, Yc - y))
    puntos.append((Xc - x, Yc - y))

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

# Función para rellenar la elipse
def rellenar_elipse(puntos_borde, Xc, Yc):
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
def imprimir_tablas(region1, region2, Xc, Yc):
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

    tab1 = ttk.Frame(tab_control)
    tab2 = ttk.Frame(tab_control)
    tab_control.add(tab1, text="Región 1")
    tab_control.add(tab2, text="Región 2")
    tab_control.pack(expand=1, fill='both')

    headers = ["K", "Pk", "Xk", "Yk"]
    tree1 = ttk.Treeview(tab1, columns=headers, show='headings')
    tree2 = ttk.Treeview(tab2, columns=headers, show='headings')
    for header in headers:
        tree1.heading(header, text=header)
        tree1.column(header, anchor='center')
        tree2.heading(header, text=header)
        tree2.column(header, anchor='center')
    tree1.pack(expand=1, fill='both')
    tree2.pack(expand=1, fill='both')

    for k, (x, y, p) in enumerate(region1):
        tree1.insert("", "end", values=(k, p, x, y))

    for k, (x, y, p) in enumerate(region2):
        tree2.insert("", "end", values=(k, p, x, y))

    root.mainloop()

# Función para graficar la elipse de manera animada
def graficar_elipse_animada(puntos_relleno, puntos_borde, Xc, Yc, Rx, Ry):
    fig, ax = plt.subplots()
    ax.set_aspect('equal', adjustable='box')
    ax.grid(True)
    ax.set_xlim(Xc - Rx - 1, Xc + Rx + 1)
    ax.set_ylim(Yc - Ry - 1, Yc + Ry + 1)

    x_vals_relleno = [p[0] for p in puntos_relleno]
    y_vals_relleno = [p[1] for p in puntos_relleno]

    x_vals_borde = [p[0] for p in puntos_borde]
    y_vals_borde = [p[1] for p in puntos_borde]

    relleno = ax.scatter([], [], color='r')
    borde = ax.scatter([], [], color='b')

    plt.figtext(0.5, 0.98, 'Hecho por Jared Salazar', ha='center', fontsize=8)
    plt.figtext(0.5, 0.95, f'Centro: ({Xc}, {Yc})  Rx: {Rx}  Ry: {Ry}', ha='center', fontsize=12)

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

# Función para solicitar los parámetros de la elipse al usuario
def solicitar_parametros():
    def obtener_parametros():
        Xc = entry_Xc.get()
        Yc = entry_Yc.get()
        Rx = entry_Rx.get()
        Ry = entry_Ry.get()
        
        # Verificamos si los valores son válidos
        try:
            Xc, Yc, Rx, Ry = int(Xc), int(Yc), int(Rx), int(Ry)
            print(f"Centro: ({Xc}, {Yc}), Rx: {Rx}, Ry: {Ry}")
            
            # Llamar al algoritmo principal con los parámetros
            puntos_borde, region1, region2 = algoritmo_punto_medio_elipse(Xc, Yc, Rx, Ry)
            puntos_relleno = rellenar_elipse(puntos_borde, Xc, Yc)

            # Ejecutar funciones en paralelo
            hilo_tablas = threading.Thread(target=imprimir_tablas, args=(region1, region2, Xc, Yc))
            hilo_animacion = threading.Thread(target=graficar_elipse_animada, args=(puntos_relleno, puntos_borde, Xc, Yc, Rx, Ry))

            hilo_tablas.start()
            hilo_animacion.start()

        except ValueError:
            print("Por favor, introduce valores numéricos válidos.")
        
        # Limpiar los campos de entrada para nuevos valores
        entry_Xc.delete(0, tk.END)
        entry_Yc.delete(0, tk.END)
        entry_Rx.delete(0, tk.END)
        entry_Ry.delete(0, tk.END)

    def focus_next_widget(event):
        event.widget.tk_focusNext().focus()
        return "break"

    root = tk.Tk()
    root.title("Parámetros de la Elipse")

    # Centrar la ventana de entrada en la pantalla
    window_width = 300
    window_height = 200
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

    tk.Label(root, text="Radio X (Rx):").grid(row=2, column=0)
    entry_Rx = tk.Entry(root)
    entry_Rx.grid(row=2, column=1)
    entry_Rx.bind("<Return>", focus_next_widget)

    tk.Label(root, text="Radio Y (Ry):").grid(row=3, column=0)
    entry_Ry = tk.Entry(root)
    entry_Ry.grid(row=3, column=1)
    entry_Ry.bind("<Return>", focus_next_widget)

    tk.Button(root, text="Aceptar", command=obtener_parametros).grid(row=4, columnspan=2)

    root.mainloop()

# Función principal
def main():
    # Solicitar al usuario los parámetros de la elipse
    solicitar_parametros()

if __name__ == "__main__":
    main()