# Función que implementa el algoritmo DDA para un triángulo
def algoritmo_dda_triangulo(xa, ya, xb, yb, xc, yc):
    def dda(x0, y0, x1, y1):
        x = x0
        y = y0
        puntos = [(round(x, 3), round(y, 3))]
        dx = x1 - x0
        dy = y1 - y0
        
        if dx == 0:
            paso_y = 1 if y1 > y0 else -1
            for _ in range(abs(dy)):
                y += paso_y
                puntos.append((round(x, 3), round(y, 3)))
            return puntos
        
        pasos = max(abs(dx), abs(dy))
        incremento_x = dx / pasos
        incremento_y = dy / pasos
        for _ in range(int(pasos)):
            x += incremento_x
            y += incremento_y
            puntos.append((round(x, 3), round(y, 3)))
        return puntos
    
    puntos_ab = dda(xa, ya, xb, yb)
    puntos_bc = dda(xb, yb, xc, yc)
    puntos_ca = dda(xc, yc, xa, ya)
    
    return puntos_ab, puntos_bc, puntos_ca

# Función que determina el caso de la pendiente
def determinar_caso(x0, y0, x1, y1):
    # Si las coordenadas x son iguales, la pendiente es indefinida (línea vertical)
    if x1 == x0:
        if y1 > y0:
            return "Pendiente indefinida (vertical, m = ∞), de abajo hacia arriba"
        elif y1 < y0:
            return "Pendiente indefinida (vertical, m = ∞), de arriba hacia abajo"
        else:
            return "Error: Los puntos son idénticos"
    
    # Si las coordenadas y son iguales, la pendiente es 0 (línea horizontal)
    elif y1 == y0:
        if x1 > x0:
            return "Pendiente igual a 0 (horizontal, m = 0), de izquierda a derecha"
        else:
            return "Pendiente igual a 0 (horizontal, m = 0), de derecha a izquierda"
    
    # Calcula la pendiente m
    m = (y1 - y0) / (x1 - x0)
    
    # Determina el caso basado en el valor de la pendiente m y las posiciones relativas de los puntos
    if m == 1:
        if x1 > x0 and y1 > y0:
            return "Pendiente igual a 1 (m = 1), de izquierda a derecha y de abajo hacia arriba"
        elif x1 < x0 and y1 < y0:
            return "Pendiente igual a 1 (m = 1), de derecha a izquierda y de arriba hacia abajo"
    elif m == -1:
        if x1 > x0 and y1 < y0:
            return "Pendiente igual a -1 (m = -1), de izquierda a derecha y de arriba hacia abajo"
        elif x1 < x0 and y1 > y0:
            return "Pendiente igual a -1 (m = -1), de derecha a izquierda y de abajo hacia arriba"
    elif 0 < m < 1:
        if x1 > x0:
            return "Pendiente positiva menor que 1 (0 < m < 1), de izquierda a derecha y de abajo hacia arriba"
        else:
            return "Pendiente positiva menor que 1 (0 < m < 1), de derecha a izquierda y de arriba hacia abajo"
    elif m > 1:
        if x1 > x0:
            return "Pendiente positiva mayor que 1 (m > 1), de izquierda a derecha y de abajo hacia arriba"
        else:
            return "Pendiente positiva mayor que 1 (m > 1), de derecha a izquierda y de abajo hacia arriba"
    elif m < -1:
        if x1 > x0:
            return "Pendiente negativa menor que -1 (m < -1), de izquierda a derecha y de arriba hacia abajo"
        else:
            return "Pendiente negativa menor que -1 (m < -1), de derecha a izquierda y de abajo hacia arriba"
    elif -1 < m < 0:
        if x1 > x0:
            return "Pendiente negativa mayor que -1 (-1 < m < 0), de izquierda a derecha y de arriba hacia abajo"
        else:
            return "Pendiente negativa mayor que -1 (-1 < m < 0), de derecha a izquierda y de abajo hacia arriba"
    else:
        return "Caso no determinado"

# Función que determina el caso del triángulo
def determinar_caso_triangulo(xa, ya, xb, yb, xc, yc):
    casos = {
        'AB': determinar_caso(xa, ya, xb, yb),
        'BC': determinar_caso(xb, yb, xc, yc),
        'CA': determinar_caso(xc, yc, xa, ya)
    }
    
    return casos

# Función para rellenar el triángulo
def rellenar_triangulo(xa, ya, xb, yb, xc, yc):
    puntos_ab, puntos_bc, puntos_ca = algoritmo_dda_triangulo(xa, ya, xb, yb, xc, yc)
    
    # Combina todos los puntos de las líneas
    puntos = set(puntos_ab + puntos_bc + puntos_ca)
    
    # Rellenar el triángulo
    for y in range(min(ya, yb, yc), max(ya, yb, yc) + 1):
        puntos_en_y = [p for p in puntos if p[1] == y]
        if len(puntos_en_y) > 1:
            x_min = min(p[0] for p in puntos_en_y)
            x_max = max(p[0] for p in puntos_en_y)
            for x in range(int(x_min), int(x_max) + 1):
                puntos.add((x, y))
    
    return sorted(puntos)

# Define los puntos del triángulo
xa, ya = 10, 10
xb, yb = 20, 20
xc, yc = 10, 20

# Llama a la función para determinar el caso del triángulo
casos = determinar_caso_triangulo(xa, ya, xb, yb, xc, yc)
print(f"Casos del triángulo: {casos}")

# Llama a la función para rellenar el triángulo
puntos_triangulo = rellenar_triangulo(xa, ya, xb, yb, xc, yc)

# Imprime los puntos del triángulo
print(f"Puntos del triángulo: {puntos_triangulo}")