# En Flask app.py
from flask import Flask, request, jsonify
from utils import cargar_departamentos, procesar_ventas, generar_xml_resumen
import xml.etree.ElementTree as ET
import os
import unicodedata

app = Flask(__name__)
departamentos = cargar_departamentos()

# Directorio para guardar el archivo XML de salida
OUTPUT_DIR = 'output'
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

@app.route('/upload-ventas', methods=['POST'])
def upload_ventas():
    if 'file' not in request.files:
        return jsonify({"error": "No se encontró el archivo"}), 400

    file = request.files['file']
    try:
        xml_data = file.read().decode('utf-8')

        if not xml_data.strip():
            return jsonify({"error": "El archivo XML está vacío."}), 400

        try:
            ET.fromstring(xml_data)
        except ET.ParseError as e:
            return jsonify({"error": f"El archivo XML no es válido: {str(e)}"}), 400

        procesar_ventas(xml_data, departamentos)
        xml_resumen = generar_xml_resumen(departamentos)
        output_file_path = os.path.join(OUTPUT_DIR, 'resumen_ventas.xml')
        
        # Abrir el archivo en modo 'w' para vaciar el contenido antes de escribir nuevos datos
        with open(output_file_path, 'w', encoding='utf-8') as f:
            f.write('')  # Esto vacía el archivo
            f.write(xml_resumen)  # Escribe los nuevos datos en el archivo vacío

        return jsonify({"message": "Archivo procesado exitosamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/resumen-ventas', methods=['GET'])
def resumen_ventas():
    try:
        # Leer el archivo XML de salida y devolverlo
        output_file_path = os.path.join(OUTPUT_DIR, 'resumen_ventas.xml')
        with open(output_file_path, 'r', encoding='utf-8') as f:
            xml_resumen = f.read()
            print("XML de Resumen generado:")
            print(xml_resumen)
        return app.response_class(xml_resumen, content_type='application/xml')
    except Exception as e:
        return jsonify({"error": str(e)}), 500



if __name__ == '__main__':
    app.run(debug=True, port=5000)
