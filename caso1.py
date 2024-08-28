import matplotlib.pyplot as plt  # Importamos la librería matplotlib para graficar

# Definimos la función que implementa el algoritmo DDA con pendiente
def algoritmo_dda_con_pendiente(x0, y0, x1, y1, pendiente):
    # Inicialización de las coordenadas iniciales
    x = x0
    y = y0
    puntos = [(x, y)]  # Lista para almacenar los puntos de la línea
    
    # Calculamos la diferencia en las coordenadas x e y
    dx = x1 - x0
    dy = y1 - y0
    # Determinamos el número de pasos necesarios, que es el mayor valor absoluto entre dx y dy
    pasos = max(abs(dx), abs(dy))
    
    # Calculamos los incrementos en x e y por cada paso
    incremento_x = dx / pasos
    incremento_y = pendiente * incremento_x
    
    # Iteramos para calcular todos los puntos de la línea
    for _ in range(int(pasos)):
        x += incremento_x  # Incrementamos x
        y += incremento_y  # Incrementamos y
        puntos.append((round(x), round(y)))  # Añadimos el punto redondeado a la lista
    
    return puntos  # Devolvemos la lista de puntos

# Definimos la función para graficar la línea
def graficar_linea(puntos):
    # Extraemos las coordenadas x e y de los puntos
    coordenadas_x, coordenadas_y = zip(*puntos)
    # Graficamos los puntos
    plt.plot(coordenadas_x, coordenadas_y, marker='o')
    plt.title('Línea generada por el algoritmo DDA con pendiente')  # Título del gráfico
    plt.xlabel('X')  # Etiqueta del eje X
    plt.ylabel('Y')  # Etiqueta del eje Y
    plt.grid(True)  # Mostramos la cuadrícula
    plt.show()  # Mostramos el gráfico

# Función principal del programa
def main():
    # Solicitamos al usuario las coordenadas del punto A
    x0, y0 = map(int, input("Ingrese las coordenadas del punto A (x0 y0) separadas por espacio: ").split())
    # Solicitamos al usuario las coordenadas del punto B
    x1, y1 = map(int, input("Ingrese las coordenadas del punto B (x1 y1) separadas por espacio: ").split())
    
    # Calculamos la pendiente inicial entre los puntos A y B
    dx = x1 - x0
    dy = y1 - y0
    pendiente_inicial = dy / dx if dx != 0 else float('inf')  # Evitamos la división por cero
    print(f"La pendiente calculada entre los puntos A y B es: {pendiente_inicial}")
    
    # Solicitamos al usuario que ingrese una pendiente personalizada
    pendiente = float(input("Ingrese el valor de la pendiente (M): "))
    
    # Calculamos los puntos de la línea usando el algoritmo DDA con la pendiente proporcionada
    puntos = algoritmo_dda_con_pendiente(x0, y0, x1, y1, pendiente)
    
    # Graficamos la línea
    graficar_linea(puntos)

# Ejecutamos la función principal si este archivo es el programa principal
if __name__ == "__main__":
    main()