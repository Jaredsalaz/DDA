from flask import Flask, render_template, request, jsonify
import json
from algoritmo import (
    algoritmo_punto_medio_elipse,
    linea_dda,
    rellenar_elipse,
    imprimir_tablas,
    graficar_elipse_animada
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

# Define la ruta para calcular los puntos de la elipse usando el método del punto medio
@app.route('/calcular_puntos_elipse', methods=['POST'])
def calcular_puntos_elipse():
    # Carga los datos JSON enviados en la solicitud POST
    data = json.loads(request.data)
    Xc = int(data['Xc'])
    Yc = int(data['Yc'])
    Rx = int(data['Rx'])
    Ry = int(data['Ry'])
    
    # Llama a la función para calcular los puntos de la elipse usando el algoritmo del punto medio
    puntos_borde, region1, region2 = algoritmo_punto_medio_elipse(Xc, Yc, Rx, Ry)
    puntos_relleno = rellenar_elipse(puntos_borde, Xc, Yc)
    
    # Devuelve los puntos en formato JSON
    return jsonify({
        'puntos_borde': list(puntos_borde),
        'region1': region1,
        'region2': region2,
        'puntos_relleno': list(puntos_relleno)
    })

# Función para abrir el navegador automáticamente
def open_browser():
    webbrowser.open_new('http://127.0.0.1:5000/')

# Inicia la aplicación Flask
if __name__ == '__main__':
    Timer(1, open_browser).start()
    app.run(debug=True)