from flask import Flask, render_template, request, jsonify
import json
from algoritmo import algoritmo_dda_triangulo, determinar_caso_triangulo, rellenar_triangulo
import webbrowser
from threading import Timer

# Crea una instancia de la aplicación Flask
app = Flask(__name__)

# Define la ruta para la página principal
@app.route('/')
def home():
    # Renderiza la plantilla 'home.html' cuando se accede a la ruta principal
    return render_template('home.html')

# Define la ruta para calcular los puntos del triángulo usando el método DDA
@app.route('/calcular_puntos_triangulo', methods=['POST'])
def calcular_puntos_triangulo():
    # Carga los datos JSON enviados en la solicitud POST
    data = json.loads(request.data)
    xa = int(data['xa'])
    ya = int(data['ya'])
    xb = int(data['xb'])
    yb = int(data['yb'])
    xc = int(data['xc'])
    yc = int(data['yc'])
    
    # Llama a la función para calcular los puntos del triángulo usando el algoritmo DDA
    puntos_ab, puntos_bc, puntos_ca = algoritmo_dda_triangulo(xa, ya, xb, yb, xc, yc)
    
    # Determina el caso específico del triángulo
    casos = determinar_caso_triangulo(xa, ya, xb, yb, xc, yc)
    
    # Rellena el triángulo
    puntos_relleno = rellenar_triangulo(xa, ya, xb, yb, xc, yc)
    
    # Devuelve los puntos y el caso en formato JSON
    return jsonify({
        'puntos_ab': puntos_ab,
        'puntos_bc': puntos_bc,
        'puntos_ca': puntos_ca,
        'casos': casos,
        'puntos_relleno': puntos_relleno
    })

# Función para abrir el navegador automáticamente
def open_browser():
    webbrowser.open_new('http://127.0.0.1:5000/')

# Inicia la aplicación Flask
if __name__ == '__main__':
    Timer(1, open_browser).start()
    app.run(debug=True)