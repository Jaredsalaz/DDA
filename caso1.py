import tkinter as tk
from tkinter import simpledialog, messagebox
import matplotlib.pyplot as plt

# Definimos la función que implementa el algoritmo DDA con pendiente
def algoritmo_dda_con_pendiente(x0, y0, x1, y1, pendiente):
    x = x0
    y = y0
    puntos = [(x, y)]
    dx = x1 - x0
    dy = y1 - y0
    pasos = max(abs(dx), abs(dy))
    incremento_x = dx / pasos
    incremento_y = pendiente * incremento_x
    for _ in range(int(pasos)):
        x += incremento_x
        y += incremento_y
        puntos.append((round(x), round(y)))
    return puntos

# Definimos la función para graficar la línea
def graficar_linea(puntos):
    coordenadas_x, coordenadas_y = zip(*puntos)
    plt.plot(coordenadas_x, coordenadas_y, marker='o')
    plt.title('Línea generada por el algoritmo DDA con pendiente')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.grid(True)
    plt.show()

# Función principal del programa
def main_program():
    try:
        # Solicitar las coordenadas del punto A
        x0 = int(simpledialog.askstring("Entrada", "Ingrese la coordenada x0 del punto A:"))
        y0 = int(simpledialog.askstring("Entrada", "Ingrese la coordenada y0 del punto A:"))
        
        # Solicitar las coordenadas del punto B
        x1 = int(simpledialog.askstring("Entrada", "Ingrese la coordenada x1 del punto B:"))
        y1 = int(simpledialog.askstring("Entrada", "Ingrese la coordenada y1 del punto B:"))
        
        # Calcular la pendiente inicial
        dx = x1 - x0
        dy = y1 - y0
        pendiente_inicial = dy / dx if dx != 0 else float('inf')
        messagebox.showinfo("Pendiente Calculada", f"La pendiente calculada entre los puntos A y B es: {pendiente_inicial}")
        
        # Solicitar la pendiente personalizada
        pendiente = float(simpledialog.askstring("Entrada", "Ingrese el valor de la pendiente (M):"))
        
        # Calcular los puntos de la línea
        puntos = algoritmo_dda_con_pendiente(x0, y0, x1, y1, pendiente)
        
        # Graficar la línea
        graficar_linea(puntos)
    except Exception as e:
        messagebox.showerror("Error", f"Ha ocurrido un error: {e}")

# Función para iniciar el programa desde la interfaz gráfica
def iniciar_programa():
    ventana.destroy()
    main_program()

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Caso 1: Recta")
ventana.geometry("400x300")
ventana.configure(bg="#f0f0f0")

# Crear un marco para centrar el contenido
frame = tk.Frame(ventana, bg="#f0f0f0")
frame.pack(expand=True)

# Etiqueta del título del programa
titulo = tk.Label(frame, text="Caso 1: Recta", font=("Helvetica", 24, "bold"), bg="#f0f0f0")
titulo.pack(pady=20)

# Etiqueta del nombre del alumno
nombre_alumno = tk.Label(frame, text="Jared Daniel Salazar Sanchez", font=("Helvetica", 14), bg="#f0f0f0")
nombre_alumno.pack(pady=10)

# Botón para iniciar el programa
boton_iniciar = tk.Button(frame, text="Iniciar Programa", font=("Helvetica", 14), command=iniciar_programa, bg="#4CAF50", fg="white", activebackground="#45a049", padx=10, pady=5)
boton_iniciar.pack(pady=20)

# Ejecutar la ventana principal
ventana.mainloop()