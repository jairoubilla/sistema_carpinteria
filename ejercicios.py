nombre_cliente = "Juan"
apellido_cliente = "Perez"
telefono_cliente = "+549233445"
direccion_cliente = "calle 1"
dni_cliente = "21345678"

mueble_ot1 = "mesa de roble"
cant_patas = 4
costo_total = 45000.50
senia_adelanto = True

precio_total = 150000.0
adelanto_pagado = 150000.0

saldo_pendiente = precio_total - adelanto_pagado

if saldo_pendiente == 0:
    estado_entrega = "Autorizado"
else:
    estado_entrega = "Retenido"

def calcular_saldo_pendiente(total, adelanto):
    saldo = total - adelanto
    return saldo

estados_posibles_ot = ["Pendiente", "En proceso", "Terminado", "Entregado"]

cliente_nuevo = {
    "nombre": "Pedro",
    "telefono": "+54911223344",
    "presupuestos_pedidos": 1
}

precios_materiales = [12000.50, 4500.0, 8000.0]
costo_total = 0.0

for material in precios_materiales:
    costo_total = costo_total + material
    
print("*************************")
    
class Cliente:
    def __init__(self, nombre_ingresado, telefono_ingresado):
        self.nombre = nombre_ingresado
        self.telefono = telefono_ingresado
        self.presupuestos_pedidos = 0
        
    def registrar_presupuesto(self):
        self.presupuestos_pedidos += 1
        
class Presupuesto:
    def __init__(self, cliente_asignado, total_calculado):
        self.cliente = cliente_asignado
        self.total = total_calculado
        self.estado = "Pendiente"
        
cliente_ana = Cliente("Ana", "2604546798")

cliente_ana.registrar_presupuesto()

presupuesto_1 = Presupuesto(cliente_ana, 85000.0)

telefono_contacto = presupuesto_1.cliente.telefono