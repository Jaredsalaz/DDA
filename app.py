from flask import Flask, render_template, request, jsonify
import json
from algoritmo import algoritmo_dda_con_pendiente, determinar_caso
import webbrowser
from threading import Timer

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/calcular_puntos', methods=['POST'])
def calcular_puntos():
    data = json.loads(request.data)
    x0 = int(data['x0'])
    y0 = int(data['y0'])
    x1 = int(data['x1'])
    y1 = int(data['y1'])
    pendiente = (y1 - y0) / (x1 - x0) if (x1 - x0) != 0 else float('inf')
    puntos = algoritmo_dda_con_pendiente(x0, y0, x1, y1)
    caso = determinar_caso(x0, y0, x1, y1)
    return jsonify({'puntos': puntos, 'pendiente': round(pendiente, 4), 'caso': caso})

def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000")

if __name__ == '__main__':
    # Desactiva el reinicio automático del servidor de Flask
    app.config['TEMPLATES_AUTO_RELOAD'] = False
    app.config['DEBUG'] = False
    
    # Asegúrate de que el navegador solo se abra una vez
    Timer(1, open_browser).start()
    app.run(port=5000)