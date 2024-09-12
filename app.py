from flask import Flask, render_template, request, jsonify
import json
from algoritmo import algoritmo_dda_con_pendiente, determinar_caso
import webbrowser
from threading import Timer

# Crea una instancia de la aplicación Flask
app = Flask(__name__)

# Define la ruta para la página principal
@app.route('/')
def home():
    # Renderiza la plantilla 'home.html' cuando se accede a la ruta principal
    return render_template('home.html')

# Define la ruta para calcular los puntos usando el método DDA
@app.route('/calcular_puntos', methods=['POST'])
def calcular_puntos():
    # Carga los datos JSON enviados en la solicitud POST
    data = json.loads(request.data)
    x0 = int(data['x0'])
    y0 = int(data['y0'])
    x1 = int(data['x1'])
    y1 = int(data['y1'])
    
    # Calcula la pendiente de la línea
    pendiente = (y1 - y0) / (x1 - x0) if (x1 - x0) != 0 else float('inf')
    
    # Llama a la función para calcular los puntos usando el algoritmo DDA
    puntos = algoritmo_dda_con_pendiente(x0, y0, x1, y1)
    
    # Determina el caso específico del algoritmo
    caso = determinar_caso(x0, y0, x1, y1)
    
    # Devuelve los puntos, la pendiente y el caso en formato JSON
    return jsonify({'puntos': puntos, 'pendiente': round(pendiente, 4), 'caso': caso})

# Función para abrir el navegador web automáticamente
def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000")

if __name__ == '__main__':
    # Desactiva el reinicio automático del servidor de Flask
    app.config['TEMPLATES_AUTO_RELOAD'] = False
    app.config['DEBUG'] = False
    
    # Asegúrate de que el navegador solo se abra una vez
    Timer(1, open_browser).start()
    
    # Inicia la aplicación Flask en el puerto 5000
    app.run(port=5000)