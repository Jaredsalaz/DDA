import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

def plot_circle_points(Xc, Yc, x, y, octantes):
    octantes[0].append((Xc + x, Yc + y))
    octantes[1].append((Xc - x, Yc + y))
    octantes[2].append((Xc + x, Yc - y))
    octantes[3].append((Xc - x, Yc - y))
    octantes[4].append((Xc + y, Yc + x))
    octantes[5].append((Xc - y, Yc + x))
    octantes[6].append((Xc + y, Yc - x))
    octantes[7].append((Xc - y, Yc - x))

def midpoint_circle_algorithm(Xc, Yc, r):
    x = 0
    y = r
    p = 1 - r
    puntos = [(x, y, p)]
    octantes = [[] for _ in range(8)]

    plot_circle_points(Xc, Yc, x, y, octantes)

    while x < y:
        x += 1
        if p < 0:
            p = p + 2 * x + 1
        else:
            y -= 1
            p = p + 2 * x + 1 - 2 * y
        puntos.append((x, y, p))
        plot_circle_points(Xc, Yc, x, y, octantes)

    return puntos, octantes

def dda_line(x0, y0, x1, y1):
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
            puntos_relleno.update(dda_line(x_min, y, x_max, y))

    return puntos_relleno

def imprimir_tablas(puntos, Xc, Yc):
    print("N\tPk\tXk+1\tYk-1")
    for i, (x, y, p) in enumerate(puntos):
        if i == 0:
            print(f"{i}\t{p}\t{x + 1}\t{y}")
        else:
            if puntos[i-1][2] < 0:
                print(f"{i}\t{p}\t{x + 1}\t{y}")
            else:
                print(f"{i}\t{p}\t{x + 1}\t{y - 1}")

    print("\nY\tX")
    for x, y, _ in puntos:
        print(f"{y}\t{x}")

    print("\nX\t-Y")
    for x, y, _ in puntos:
        print(f"{x}\t{-y}")

    print("\n-Y\tX")
    for x, y, _ in puntos:
        print(f"{-y}\t{x}")

    print("\n-Y\t-X")
    for x, y, _ in puntos:
        print(f"{-y}\t{-x}")

    print("\n-X\t-Y")
    for x, y, _ in puntos:
        print(f"{-x}\t{-y}")

    print("\n-X\tY")
    for x, y, _ in puntos:
        print(f"{-x}\t{y}")

    print("\nY\t-X")
    for x, y, _ in puntos:
        print(f"{y}\t{-x}")

def graficar_circulo_animado(puntos_relleno, puntos_borde, Xc, Yc):
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
        return relleno, borde

    ani = animation.FuncAnimation(fig, animate, init_func=init, frames=len(x_vals_relleno), interval=50, blit=True)
    plt.show()

# Solicitar al usuario los parámetros del círculo
Xc = int(input("Ingrese la coordenada X del centro del círculo: "))
Yc = int(input("Ingrese la coordenada Y del centro del círculo: "))
r = int(input("Ingrese el radio del círculo: "))

# Obtener los puntos del círculo y los octantes
puntos, octantes = midpoint_circle_algorithm(Xc, Yc, r)

# Obtener los puntos del borde del círculo
puntos_borde = set()
for octante in octantes:
    puntos_borde.update(octante)

# Rellenar el círculo
puntos_relleno = rellenar_circulo(puntos_borde, Xc, Yc)

# Imprimir las tablas de los puntos calculados
imprimir_tablas(puntos, Xc, Yc)

# Graficar el círculo relleno con borde animado
graficar_circulo_animado(puntos_relleno, puntos_borde, Xc, Yc)