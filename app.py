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
    data = request.get_json()
    xa, ya = data['xa'], data['ya']
    xb, yb = data['xb'], data['yb']
    xc, yc = data['xc'], data['yc']
    
    # Calcula los puntos del triángulo
    puntos_ab, puntos_bc, puntos_ca = algoritmo_dda_triangulo(xa, ya, xb, yb, xc, yc)
    puntos_relleno = rellenar_triangulo(xa, ya, xb, yb, xc, yc)
    
    # Determina el caso del triángulo
    casos = determinar_caso_triangulo(xa, ya, xb, yb, xc, yc)
    
    # Devuelve los puntos y los casos como una respuesta JSON
    return jsonify({
        'puntos_ab': puntos_ab,
        'puntos_bc': puntos_bc,
        'puntos_ca': puntos_ca,
        'puntos_relleno': puntos_relleno,
        'casos': casos
    })

# Define la ruta para determinar el caso del triángulo
@app.route('/determinar_caso_triangulo', methods=['POST'])
def determinar_caso_triangulo_route():
    # Carga los datos JSON enviados en la solicitud POST
    data = request.get_json()
    xa, ya = data['xa'], data['ya']
    xb, yb = data['xb'], data['yb']
    xc, yc = data['xc'], data['yc']
    
    # Determina el caso del triángulo
    casos = determinar_caso_triangulo(xa, ya, xb, yb, xc, yc)
    
    # Devuelve los casos como una respuesta JSON
    return jsonify(casos)

# Función para abrir el navegador automáticamente
def open_browser():
    webbrowser.open_new('http://127.0.0.1:5000/')

# Inicia la aplicación Flask
if __name__ == '__main__':
    Timer(1, open_browser).start()
    app.run(debug=True)