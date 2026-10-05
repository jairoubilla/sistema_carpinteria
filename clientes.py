
class Cliente:
    def __init__(self, nombre_ingresado, telefono_ingresado):
        self.nombre = nombre_ingresado
        self.telefono = telefono_ingresado
        self.presupuestos_pedidos = 0
        
    def registrar_presupuesto(self):
        self.presupuestos_pedidos += 1