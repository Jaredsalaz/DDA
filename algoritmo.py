# Función que implementa el algoritmo DDA
def algoritmo_dda_con_pendiente(x0, y0, x1, y1):
    # Inicializa las coordenadas x e y con los valores iniciales
    x = x0
    y = y0
    # Crea una lista de puntos y añade el punto inicial redondeado a 4 decimales
    puntos = [(round(x, 4), round(y, 4))]
    # Calcula la diferencia en x y en y entre los puntos finales e iniciales
    dx = x1 - x0
    dy = y1 - y0
    
    # Si dx es 0, significa que la línea es vertical
    if dx == 0:
        # Determina la dirección de la línea vertical
        paso_y = 1 if y1 > y0 else -1
        for _ in range(abs(dy)):
            y += paso_y
            puntos.append((round(x, 4), round(y, 4)))
        return puntos
    
    # Determina el número de pasos necesarios como el máximo valor absoluto entre dx y dy
    pasos = max(abs(dx), abs(dy))
    # Calcula los incrementos en x e y por cada paso
    incremento_x = dx / pasos
    incremento_y = dy / pasos
    # Itera desde 0 hasta el número de pasos
    for _ in range(int(pasos)):
        # Incrementa x e y por sus respectivos incrementos
        x += incremento_x
        y += incremento_y
        # Añade el nuevo punto redondeado a 4 decimales a la lista de puntos
        puntos.append((round(x, 4), round(y, 4)))
    # Retorna la lista de puntos calculados
    return puntos

# Función que determina el caso de la pendiente
def determinar_caso(x0, y0, x1, y1):
    # Si las coordenadas x son iguales, la pendiente es indefinida (línea vertical)
    if x1 == x0:
        if y1 > y0:
            return "Pendiente indefinida (vertical, m = ∞), de abajo hacia arriba"
        else:
            return "Pendiente indefinida (vertical, m = ∞), de arriba hacia abajo"
    
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
        elif x1 > x0 and y1 < y0:
            return "Pendiente igual a 1 (m = 1), de izquierda a derecha y de arriba hacia abajo"
        elif x1 < x0 and y1 > y0:
            return "Pendiente igual a 1 (m = 1), de derecha a izquierda y de abajo hacia arriba"
    elif m == -1:
        if x1 > x0 and y1 < y0:
            return "Pendiente igual a -1 (m = -1), de izquierda a derecha y de arriba hacia abajo"
        elif x1 < x0 and y1 > y0:
            return "Pendiente igual a -1 (m = -1), de derecha a izquierda y de abajo hacia arriba"
        elif x1 > x0 and y1 > y0:
            return "Pendiente igual a -1 (m = -1), de izquierda a derecha y de abajo hacia arriba"
        elif x1 < x0 and y1 < y0:
            return "Pendiente igual a -1 (m = -1), de derecha a izquierda y de arriba hacia abajo"
    elif 0 < m < 1:
        if x1 > x0:
            return "1 Pendiente positiva menor que 1 (0 < m < 1), de izquierda a derecha y de abajo hacia arriba"
        else:
            return "2 Pendiente positiva menor que 1 (0 < m < 1), de derecha a izquierda y de arriba hacia abajo"
    elif m > 1:
        if x1 > x0:
            return "3 Pendiente positiva mayor que 1 (m > 1), de izquierda a derecha y de abajo hacia arriba"
        else:
            return "4 Pendiente positiva mayor que 1 (m > 1), de derecha a izquierda y de abajo hacia arriba"
    elif m < -1:
        if x1 > x0 and y1 > y0:
            return "Pendiente negativa menor que -1 (m < -1), de izquierda a derecha y de abajo hacia arriba"
        elif x1 < x0 and y1 < y0:
            return "Pendiente negativa menor que -1 (m < -1), de derecha a izquierda y de arriba hacia abajo"
        elif x1 > x0 and y1 < y0:
            return "4 Pendiente negativa menor que -1 (m < -1), de izquierda a derecha y de arriba hacia abajo"
        elif x1 < x0 and y1 > y0:
            return "3 Pendiente negativa menor que -1 (m < -1), de derecha a izquierda y de abajo hacia arriba"
    elif -1 < m < 0:
        if x1 > x0:
            return "2 Pendiente negativa mayor que -1 (-1 < m < 0), de izquierda a derecha y de arriba hacia abajo"
        else:
            return "1 Pendiente negativa mayor que -1 (-1 < m < 0), de derecha a izquierda y de abajo hacia arriba"
    else:
        return "Caso no determinado"
    
# Define los puntos iniciales y finales
x0, y0, x1, y1 = 35, 27, 35, 22

# Llama a la función para calcular los puntos usando el algoritmo DDA
puntos = algoritmo_dda_con_pendiente(x0, y0, x1, y1)

# Llama a la función para determinar el caso de la pendiente
caso = determinar_caso(x0, y0, x1, y1)

# Imprime los puntos calculados y el caso determinado
print(f"Puntos: {puntos}")
print(f"Caso: {caso}")