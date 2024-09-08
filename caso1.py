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

def determinar_caso(x0, y0, x1, y1):
    if x1 == x0:
        return "Pendiente indefinida (vertical, m = ∞)"
    elif y1 == y0:
        return "Pendiente igual a 0 (horizontal, m = 0)"
    
    m = (y1 - y0) / (x1 - x0)
    
    if m == 1:
        if x1 > x0 and y1 > y0:
            return "Pendiente igual a 1 (m = 1), de izquierda a derecha y de abajo hacia arriba"
        elif x1 < x0 and y1 < y0:
            return "Pendiente igual a 1 (m = 1), de derecha a izquierda y de arriba hacia abajo"
        elif x1 > x0 and y1 < y0:
            return "Pendiente igual a 1 (m = 1), de izquierda a derecha y de arriba hacia abajo"
        elif x1 < x0 and y1 > y0:
            return "Pendiente igual a 1 (m = 1), de derecha a izquierda y de abajo hacia arriba"
    elif 0 < m < 1:
        if x1 > x0:
            return "Pendiente positiva menor que 1 (0 < m < 1), de izquierda a derecha y de abajo hacia arriba"
        else:
            return "Pendiente positiva menor que 1 (0 < m < 1), de derecha a izquierda y de arriba hacia abajo"
    elif m > 1:
        if x1 > x0:
            return "Pendiente positiva mayor que 1 (m > 1), de izquierda a derecha y de abajo hacia arriba"
        else:
            return "Pendiente positiva mayor que 1 (m > 1), de derecha a izquierda y de arriba hacia abajo"
    elif m < -1:
        if x1 > x0:
            return "Pendiente negativa menor que -1 (m < -1), de izquierda a derecha y de abajo hacia arriba"
        else:
            return "Pendiente negativa menor que -1 (m < -1), de derecha a izquierda y de arriba hacia abajo"
    elif -1 < m < 0:
        if x1 > x0:
            return "Pendiente negativa mayor que -1 (-1 < m < 0), de izquierda a derecha y de arriba hacia abajo"
        else:
            return "Pendiente negativa mayor que -1 (-1 < m < 0), de derecha a izquierda y de abajo hacia arriba"
    else:
        return "Caso no determinado"

# Ejemplo de uso
x0, y0, x1, y1 = 0, 0, 5, 5
puntos = algoritmo_dda_con_pendiente(x0, y0, x1, y1)
caso = determinar_caso(x0, y0, x1, y1)
print(f"Puntos: {puntos}")
print(f"Caso: {caso}")