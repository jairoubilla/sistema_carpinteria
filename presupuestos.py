import datetime
import random
from dinero import Finanzas


class Presupuesto:
    def __init__(self, cliente_asignado, total_calculado, id_orden=None):
        self.cliente = cliente_asignado
        self.fecha = datetime.date.today().strftime("%d/%m/%Y")
        self.total = total_calculado
        self.estado = "Pendiente"
        self.finanzas = Finanzas(total_calculado)
        
        if id_orden is None:
            self.id_orden = random.randint(1000, 9999)
        else:
            self.id_orden = id_orden
        
    def actualizar_estado(self, nuevo_estado):
        self.estado = nuevo_estado