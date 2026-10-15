from clientes import Cliente
from presupuestos import Presupuesto

clientes_registrados = []
presupuestos_registrados = []

# --- RUTINA DE ARRANQUE ---
try:
    with open("historial_presupuestos.txt", "r") as archivo:
        for linea in archivo:
            # 1. Limpiamos el Enter (\n) del final de la línea
            linea_limpia = linea.strip()
            
            # 2. Cortamos la línae por los guiones "-"
            # Esto crea una lista de 4 elementos: ["Cliente: nombre", " Telefono: telefono", " Presupuesto: monto", " Estado: estado"]
            partes = linea_limpia.split("-")
            
            # 3. De cada parte, cortamos por los dos puntos ":" y nos quedamos con el segundo elemento (índice 1) que es el valor
            nombre_guardado = partes[0].split(": ")[1]
            telefono_guardado = partes[1].split(": ")[1]
            monto_guardado = float(partes[2].split(": ")[1]) # Comvertimos a número porque es dinero!
            estado_guardado = partes[3].split(": ")[1]
            
            # 4. Reconstruimos los objetos usando las Clases
            cliente_recuperado = Cliente(nombre_guardado, telefono_guardado)
            presu_recuperado = Presupuesto(cliente_recuperado, monto_guardado)
            
            # 5. Los guardamos en las listas de la memoria RAM
            clientes_registrados.append(cliente_recuperado)
            presupuestos_registrados.append(presu_recuperado)
        
    print(f"SISTEMA INICIADO: Se recuperaron {len(presupuestos_registrados)} presupuestos de la base de datos.")
except FileNotFoundError:
    print("SISTEMA INICIADO: Base de datos nueva. No se encontraron presupuestos previos.")

# --- MENU PRINCIPAL ---

while True:
    print("---BIENVENIDO AL SISTEMA DE GESTIÓN DE CARPINTERÍA---")
    print("1. Registrar nuevo presupuesto")
    print("2. Ver todos los presupuestos")
    print("3. Ver historial completo")
    print("4. Salir")
    
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
        print(f"Seña requerida: ${nuevo_presupuesto.finanzas.sena_requerida}")
        print(f"Saldo pendiente: ${nuevo_presupuesto.finanzas.saldo_pendiente}")
        
        with open("historial_presupuestos.txt", "a") as archivo:
            archivo.write(f"Cliente: {nuevo_cliente.nombre} - Telefono: {nuevo_cliente.telefono} - Presupuesto: {nuevo_presupuesto.total} - Estado: {nuevo_presupuesto.estado}\n")
        
    elif opcion == "2":
        for presu in presupuestos_registrados:
            print(f"Presupuesto: {presu.total} - Cliente: {presu.cliente.nombre} - Estado: {presu.estado}")
    elif opcion == "3":
        try:
            with open("historial_presupuestos.txt", "r") as archivo:
                historial = archivo.read()
                print("---HISTORIAL HISTÓRICO ---")
                print(historial)
        except FileNotFoundError:
            print("No hay historial disponible.")
    elif opcion == "4":
        print("Cerrando el sistema. ¡Hasta luego!")
        break
    else:
        print("Opción no válida. Por favor, intente nuevamente.")