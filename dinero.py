class Finanzas:
    def __init__(self, monto_total):
        self.monto_total = monto_total
        # Calculamos automáticamente el 50% para materiales
        self.sena_requerida = monto_total * 0.50
        # Al principio, deben todo el presupuesto
        self.saldo_pendiente = monto_total
        
    def registrar_pago(self, monto_pagado):
        # A lo que deben, le restamos lo que acaban de pagar
        self.saldo_pendiente -= monto_pagado