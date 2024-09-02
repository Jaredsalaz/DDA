from flask import Flask, render_template, request, jsonify
import json
from caso1 import algoritmo_dda_con_pendiente
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
    return jsonify({'puntos': puntos, 'pendiente': round(pendiente, 4)})

def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000")

if __name__ == '__main__':
    Timer(1, open_browser).start()
    app.run(debug=True, port=5000)
    # flask run --debugg