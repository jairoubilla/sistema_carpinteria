from clientes import Cliente
from presupuestos import Presupuesto

primer_cliente = Cliente("Juan", "+54911223344")
nuevo_presupuesto = Presupuesto(primer_cliente, 85000.0)

primer_cliente.registrar_presupuesto()

print(f"Presupuestos pedidos por {primer_cliente.nombre}: {primer_cliente.presupuestos_pedidos}")
print(f"El presupuesto para {nuevo_presupuesto.cliente.nombre} es de ${nuevo_presupuesto.total} y esta {nuevo_presupuesto.estado}")