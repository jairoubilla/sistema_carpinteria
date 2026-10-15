from dinero import Finanzas

class Presupuesto:
    def __init__(self, cliente_asignado, total_calculado):
        self.cliente = cliente_asignado
        self.total = total_calculado
        self.estado = "Pendiente"
        self.finanzas = Finanzas(total_calculado)