from flask import *
import xml.etree.ElementTree as ET
from backend.venta import Venta

app = Flask(__name__)
global ventas
ventas = []
@app.route('/upload-ventas', methods=['POST'])
def upload_ventas():
    file = request.files['file']
    tree = ET.parse(file)
    root = tree.getroot()

    for venta in root.findall('venta'):
        departamento = venta.find('departamento').text
        fecha = venta.find('fecha').text

        if departamento in departamentos_validos:
            ventas.append(Venta(fecha, departamento))
    return jsonify({"message": "Archivo procesado exitosamente"})