from django.shortcuts import render
from .forms import UploadFileForm
import requests
import xml.etree.ElementTree as ET
import json 

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # Obtener el archivo XML desde el formulario
            file = request.FILES['file']

            # Verificar si el archivo no está vacío
            if file.size == 0:
                error = "El archivo está vacío. Por favor, suba un archivo XML válido."
                return render(request, 'ventas/upload_failure.html', {'error': error})

            # Leer el contenido del archivo XML
            xml_content = file.read().decode('utf-8')

            # Enviar el archivo al backend Flask (localhost:5000/upload-ventas)
            files = {'file': (file.name, xml_content, 'application/xml')}
            response = requests.post('http://localhost:5000/upload-ventas', files=files)

            # Verificar si la solicitud fue exitosa
            if response.status_code == 200:
                message = response.json().get('message', 'Archivo procesado exitosamente')
                return render(request, 'ventas/upload_success.html', {'message': message, 'xml_content': xml_content})
            else:
                error = response.json().get('error', 'Error procesando el archivo')
                return render(request, 'ventas/upload_failure.html', {'error': error})
    else:
        form = UploadFileForm()
    
    return render(request, 'ventas/upload.html', {'form': form})


def resumen_ventas(request):
    response = requests.get('http://localhost:5000/resumen-ventas')
    if response.status_code == 200:
        xml_resumen = response.text
        print("XML Resumen que se está pasando a la plantilla:")
        print(xml_resumen)  # Imprimir el XML para verificar su contenido
        return render(request, 'ventas/resumen.html', {'xml_resumen': xml_resumen})
    else:
        error = 'No se pudo obtener el resumen de ventas.'
        return render(request, 'ventas/resumen.html', {'error': error})

def grafico(request):
    response = requests.get('http://localhost:5000/resumen-ventas')
    if response.status_code == 200:
        xml_resumen = response.text
        datos_procesados = procesar_datos_xml(xml_resumen)

        # Convertir los datos a formato JSON
        datos_json = json.dumps(datos_procesados)

        return render(request, 'ventas/grafico.html', {'data': datos_json})
    else:
        error = 'No se pudo obtener el resumen de ventas.'
        return render(request, 'ventas/grafico.html', {'error': error})

def datos_estudiante(request):
    return render(request, 'ventas/estudiante.html')

def base(request):
    return render(request, 'ventas/home.html')

def procesar_datos_xml(xml_resumen):
    datos = {}
    try:
        # Parsear el XML
        root = ET.fromstring(xml_resumen)

        # Encontrar el nodo de departamentos
        departamentos = root.find('departamentos')
        if departamentos is None:
            raise ValueError("No se encontraron los departamentos en el XML")

        # Iterar sobre los elementos de cada departamento
        for departamento in departamentos:
            nombre = departamento.tag  # El nombre del departamento es el nombre de la etiqueta
            ventas = int(departamento.find('cantidadVentas').text)

            # Agregar al diccionario
            datos[nombre] = ventas

    except ET.ParseError as e:
        print(f"Error al parsear el XML: {e}")
    except Exception as e:
        print(f"Error procesando los datos del XML: {e}")

    return datos