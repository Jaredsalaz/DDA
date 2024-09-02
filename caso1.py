def algoritmo_dda_con_pendiente(x0, y0, x1, y1):
    x = x0
    y = y0
    puntos = [(round(x, 4), round(y, 4))]
    dx = x1 - x0
    dy = y1 - y0
    pasos = max(abs(dx), abs(dy))
    incremento_x = dx / pasos
    incremento_y = dy / pasos
    for _ in range(int(pasos)):
        x += incremento_x
        y += incremento_y
        puntos.append((round(x, 4), round(y, 4)))
    return puntos