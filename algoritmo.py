import matplotlib.pyplot as plt

def plot_circle_points(Xc, Yc, x, y, puntos):
    puntos.append((Xc + x, Yc + y))
    puntos.append((Xc - x, Yc + y))
    puntos.append((Xc + x, Yc - y))
    puntos.append((Xc - x, Yc - y))
    puntos.append((Xc + y, Yc + x))
    puntos.append((Xc - y, Yc + x))
    puntos.append((Xc + y, Yc - x))
    puntos.append((Xc - y, Yc - x))

def midpoint_circle_algorithm(Xc, Yc, r):
    x = 0
    y = r
    p = 1 - r
    puntos = []

    plot_circle_points(Xc, Yc, x, y, puntos)

    while x < y:
        x += 1
        if p < 0:
            p += 2 * x + 1
        else:
            y -= 1
            p += 2 * x + 1 - 2 * y
        plot_circle_points(Xc, Yc, x, y, puntos)

    return puntos

def fill_circle(Xc, Yc, r):
    puntos = midpoint_circle_algorithm(Xc, Yc, r)
    puntos_relleno = set(puntos)

    for y in range(Yc - r, Yc + r + 1):
        puntos_en_y = [p for p in puntos if p[1] == y]
        if len(puntos_en_y) > 1:
            x_min = min(p[0] for p in puntos_en_y)
            x_max = max(p[0] for p in puntos_en_y)
            for x in range(x_min, x_max + 1):
                puntos_relleno.add((x, y))

    return sorted(puntos_relleno)

# Parámetros del círculo
Xc, Yc = 150, 100
r = 10

# Obtener los puntos del círculo relleno
puntos_circulo = fill_circle(Xc, Yc, r)

# Imprimir los puntos del círculo
print(f"Puntos del círculo: {puntos_circulo}")

# Graficar el círculo
x_vals = [p[0] for p in puntos_circulo]
y_vals = [p[1] for p in puntos_circulo]

plt.scatter(x_vals, y_vals, s=1)
plt.gca().set_aspect('equal', adjustable='box')
plt.show()