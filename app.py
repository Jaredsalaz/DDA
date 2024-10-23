from flask import Flask, render_template, request, jsonify
import json
from algoritmo import (
    trazar_puntos_circulo,
    algoritmo_punto_medio_circulo,
    linea_dda,
    rellenar_circulo,
    imprimir_tablas,
    graficar_circulo_animado,
    solicitar_parametros
)
import webbrowser
from threading import Timer

# Crea una instancia de la aplicación Flask
app = Flask(__name__)

# Define la ruta para la página principal
@app.route('/')
def home():
    # Renderiza la plantilla 'home.html' cuando se accede a la ruta principal
    return render_template('home.html')

# Define la ruta para calcular los puntos del círculo usando el método del punto medio
@app.route('/calcular_puntos_circulo', methods=['POST'])
def calcular_puntos_circulo():
    # Carga los datos JSON enviados en la solicitud POST
    data = json.loads(request.data)
    Xc = int(data['Xc'])
    Yc = int(data['Yc'])
    r = int(data['r'])
    
    # Llama a la función para calcular los puntos del círculo usando el algoritmo del punto medio
    puntos, octantes = algoritmo_punto_medio_circulo(Xc, Yc, r)
    puntos_borde = set()
    for octante in octantes:
        puntos_borde.update(octante)
    puntos_relleno = rellenar_circulo(puntos_borde, Xc, Yc)
    
    # Devuelve los puntos en formato JSON
    return jsonify({
        'puntos': puntos,
        'octantes': [list(octante) for octante in octantes],
        'puntos_relleno': list(puntos_relleno)
    })

# Función para abrir el navegador automáticamente
def open_browser():
    webbrowser.open_new('http://127.0.0.1:5000/')

# Inicia la aplicación Flask
if __name__ == '__main__':
    Timer(1, open_browser).start()
    app.run(debug=True)