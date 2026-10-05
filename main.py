from clientes import Cliente
from presupuestos import Presupuesto

clientes_registrados = []
presupuestos_registrados = []

while True:
    print("Bienvenido al Sistema de Gestion de Carpinteria")
    print("1. Registrar nuevo presupuesto")
    print("2. Ver todos los presupuestos")
    print("3. Salir")
    
    opcion = input("Seleccione una opción: ")
    if opcion == "1":
        nuevo_nombre = input("Ingrese el nombre del cliente: ")
        nuevo_telefono = input("Ingrese el teléfono del cliente: ")
        monto_nuevo = float(input("Ingrese el monto del presupuesto: "))

        nuevo_cliente = Cliente(nuevo_nombre, nuevo_telefono)
        nuevo_presupuesto = Presupuesto(nuevo_cliente, monto_nuevo)

        clientes_registrados.append(nuevo_cliente)
        presupuestos_registrados.append(nuevo_presupuesto)
        
        print(f"Presupuestos pedidos por {nuevo_cliente.nombre}: {nuevo_cliente.presupuestos_pedidos}")
        print(f"El presupuesto para {nuevo_presupuesto.cliente.nombre} es de ${nuevo_presupuesto.total} y esta {nuevo_presupuesto.estado}")
        
    elif opcion == "2":
        for presu in presupuestos_registrados:
            print(f"Presupuesto: {presu.total} - Cliente: {presu.cliente.nombre} - Estado: {presu.estado}")
    elif opcion == "3":
        print("Cerrando el sistema. ¡Hasta luego!")
        break
    else:
        print("Opción no válida. Por favor, intente nuevamente.")