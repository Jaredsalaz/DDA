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

# Función para verificar si un punto está dentro de un triángulo
def punto_en_triangulo(px, py, xa, ya, xb, yb, xc, yc):
    def signo(x1, y1, x2, y2, x3, y3):
        return (x1 - x3) * (y2 - y3) - (x2 - x3) * (y1 - y3)
    
    d1 = signo(px, py, xa, ya, xb, yb)
    d2 = signo(px, py, xb, yb, xc, yc)
    d3 = signo(px, py, xc, yc, xa, ya)
    
    tiene_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
    tiene_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)
    
    return not (tiene_neg and tiene_pos)

# Función para rellenar el triángulo
def rellenar_triangulo(xa, ya, xb, yb, xc, yc):
    puntos_ab, puntos_bc, puntos_ca = algoritmo_dda_triangulo(xa, ya, xb, yb, xc, yc)
    
    # Combina todos los puntos de las líneas
    puntos_borde = set(puntos_ab + puntos_bc + puntos_ca)
    puntos_relleno = set()
    
    # Encuentra los límites del triángulo
    x_min = min(p[0] for p in puntos_borde)
    x_max = max(p[0] for p in puntos_borde)
    y_min = min(p[1] for p in puntos_borde)
    y_max = max(p[1] for p in puntos_borde)
    
    # Rellenar el triángulo
    for y in range(int(y_min), int(y_max) + 1):
        puntos_en_y = [p for p in puntos_borde if int(p[1]) == y]
        if len(puntos_en_y) > 1:
            x_min_y = min(p[0] for p in puntos_en_y)
            x_max_y = max(p[0] for p in puntos_en_y)
            for x in range(int(x_min_y), int(x_max_y) + 1):
                if (x, y) not in puntos_borde and punto_en_triangulo(x, y, xa, ya, xb, yb, xc, yc):
                    puntos_relleno.add((x, y))
    
    # Combina los puntos de borde y relleno
    puntos_triangulo = sorted(puntos_borde | puntos_relleno)
    
    return puntos_triangulo