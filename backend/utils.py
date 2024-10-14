# utils.py

import json
import xml.etree.ElementTree as ET
from departamento import Departamento
from venta import Venta
import xml.dom.minidom

def cargar_departamentos():
    with open('departamentos.json', 'r') as f:
        data = json.load(f)
    return {nombre: Departamento(nombre) for nombre in data['departamentos']}

def procesar_ventas(xml_data, departamentos):
    try:
        tree = ET.ElementTree(ET.fromstring(xml_data))
        root = tree.getroot()
    except ET.ParseError as e:
        print(f"Error al parsear XML: {str(e)}")
        raise

    listado_ventas = root.find('ListadoVentas')
    if listado_ventas is None:
        raise ValueError("No se encontró el nodo 'ListadoVentas' en el XML.")
    
    for venta in listado_ventas.findall('Venta'):
        departamento_nombre = venta.get('departamento')
        if departamento_nombre in departamentos:
            departamentos[departamento_nombre].incrementar_ventas()
            print(f"Ventas incrementadas para: {departamento_nombre}. Total: {departamentos[departamento_nombre].numero_ventas}")



def generar_xml_resumen(departamentos):
    # Crear el elemento raíz <resultados>
    root = ET.Element("resultados")
    departamentos_elem = ET.SubElement(root, "departamentos")
    
    # Iterar sobre los departamentos y añadir los que tienen ventas
    for departamento in departamentos.values():
        if departamento.numero_ventas > 0:
            dep_elem = ET.SubElement(departamentos_elem, departamento.nombre.replace(" ", ""))
            cantidad_elem = ET.SubElement(dep_elem, "cantidadVentas")
            cantidad_elem.text = str(departamento.numero_ventas)
    
    # Convertir el árbol XML a una cadena de texto
    return ET.tostring(root, encoding='unicode')