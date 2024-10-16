class Departamento:
    def __init__(self, nombre, numero_ventas=0):
        self.nombre = nombre
        self.numero_ventas = numero_ventas

    def incrementar_ventas(self):
        self.numero_ventas +=1