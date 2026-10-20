from clientes import Cliente
from presupuestos import Presupuesto
import os

clientes_registrados = []
presupuestos_registrados = []

# --- RUTINA DE ARRANQUE ---
try:
    with open("historial_presupuestos.txt", "r") as archivo:
        for linea in archivo:
            # 1. Limpiamos el Enter (\n) del final de la línea
            linea_limpia = linea.strip()
            
            # Si el renglón está vacío, lo saltamos
            if linea_limpia == "":
                continue
            
            # 2. Cortamos la línae por los guiones "-"
            # Esto crea una lista de 4 elementos: ["Cliente: nombre", " Telefono: telefono", " Presupuesto: monto", " Estado: estado"]
            partes = linea_limpia.split(" - ")
            
            # 3. De cada parte, cortamos por los dos puntos ":" y nos quedamos con el segundo elemento (índice 1) que es el valor
            nombre_guardado = partes[0].split(": ")[1]
            telefono_guardado = partes[1].split(": ")[1]
            monto_guardado = float(partes[2].split(": ")[1]) # Comvertimos a número porque es dinero!
            estado_guardado = partes[3].split(": ")[1]
            saldo_guardado = float(partes[4].split(": ")[1])
            fecha_guardada = partes[5].split(": ")[1]
            
            # 4. Reconstruimos los objetos usando las Clases
            cliente_recuperado = Cliente(nombre_guardado, telefono_guardado)
            presu_recuperado = Presupuesto(cliente_recuperado, monto_guardado)
            presu_recuperado.finanzas.saldo_pendiente = saldo_guardado
            presu_recuperado.fecha = fecha_guardada
            
            # 5. Los guardamos en las listas de la memoria RAM
            clientes_registrados.append(cliente_recuperado)
            presupuestos_registrados.append(presu_recuperado)
        
    print(f"SISTEMA INICIADO: Se recuperaron {len(presupuestos_registrados)} presupuestos de la base de datos.")
except FileNotFoundError:
    print("SISTEMA INICIADO: Base de datos nueva. No se encontraron presupuestos previos.")

# --- MENU PRINCIPAL ---

while True:
    os.system("cls")
    print("")
    print("---BIENVENIDO AL SISTEMA DE GESTIÓN DE CARPINTERÍA---")
    print("")
    print("1. Registrar nuevo presupuesto")
    print("2. Ver todos los presupuestos")
    print("3. Ver historial completo")
    print("4. Registrar pago")
    print("5. Actualizar estado del trabajo")
    print("6. Eliminar presupuesto")
    print("7. Salir")
    
    opcion = input("Seleccione una opción: ")
    if opcion == "1":
        nuevo_nombre = input("Ingrese el nombre del cliente: ")
        nuevo_telefono = input("Ingrese el teléfono del cliente: ")
        
        while True:
            try:
                monto_nuevo = float(input("Ingrese el monto del presupuesto: "))
                break
            except ValueError:
                print("ERROR: Por favor, ingrese un número válido para el monto.")

        nuevo_cliente = Cliente(nuevo_nombre, nuevo_telefono)
        nuevo_presupuesto = Presupuesto(nuevo_cliente, monto_nuevo)

        clientes_registrados.append(nuevo_cliente)
        presupuestos_registrados.append(nuevo_presupuesto)

        print(f"Presupuestos pedidos por {nuevo_cliente.nombre}: {nuevo_cliente.presupuestos_pedidos}")
        print(f"El presupuesto para {nuevo_presupuesto.cliente.nombre} es de ${nuevo_presupuesto.total} y esta {nuevo_presupuesto.estado}")
        print(f"Seña requerida: ${nuevo_presupuesto.finanzas.sena_requerida}")
        print(f"Saldo pendiente: ${nuevo_presupuesto.finanzas.saldo_pendiente}")
        
        with open("historial_presupuestos.txt", "a") as archivo:
            archivo.write(f"Cliente: {nuevo_cliente.nombre} - Telefono: {nuevo_cliente.telefono} - Presupuesto: {nuevo_presupuesto.total} - Estado: {nuevo_presupuesto.estado} - Saldo: {nuevo_presupuesto.finanzas.saldo_pendiente} - Fecha: {nuevo_presupuesto.fecha}\n")
        
    elif opcion == "2":
        print("\n--- PANEL DE REPORTES ---")
        print("A. Ver TODOS los presupuestos")
        print("B. Ver trabajos ACTIVOS (Pendientes / En Proceso)")
        
        filtro = input("Seleccione un filtro (A/B): ").strip().upper()
        
        print("\n---  LISTADO DE PRESUPUESTOS ---")
        for presu in presupuestos_registrados:
            estado_limpio = presu.estado.strip().lower()
            
            print(f"DEBUG -> Filtro: [{filtro}] | Estado Limpio: [{estado_limpio}]")
            
            if filtro == "B" and estado_limpio in ["entregado", "terminado", "completado"]:
                continue # Saltamos los presupuestos que no están activos
            
            print(f"Fecha: {presu.fecha} - Presupuesto: {presu.total} - Cliente: {presu.cliente.nombre} - Estado: {presu.estado}")
            
        input("\nPresione ENTER para volver al menú principal...")
        
    elif opcion == "3":
        try:
            with open("historial_presupuestos.txt", "r") as archivo:
                historial = archivo.read()
                print("\n---HISTORIAL HISTÓRICO ---")
                print(historial)
        except FileNotFoundError:
            print("No hay historial disponible.")
        
        input("\nPresione ENTER para volver al menú principal...")
        
    elif opcion == "4":
        nombre_buscado = input("Ingrese el nombre del cliente para registrar un pago: ")
        cliente_encontrado = False # Una bandera para saber si tuvimos éxito
        
        for presu in presupuestos_registrados:
            if presu.cliente.nombre == nombre_buscado:
                cliente_encontrado = True
                print(f"Saldo actual de {nombre_buscado}: ${presu.finanzas.saldo_pendiente}")
                
                # Pedimos el pago y aplicamos el metodo de la clase Finanzas
                while True:
                    try:
                        monto_pago = float(input("Ingrese el monto del pago: "))
                        break
                    except ValueError:
                        print("ERROR: Por favor, ingrese un número válido para el monto.")
                presu.finanzas.registrar_pago(monto_pago)
                
                print(f"Pago registrado. Nuevo saldo: ${presu.finanzas.saldo_pendiente}")
                
                # Sobreescribimos el historial para reflejar el nuevo saldo
                with open("historial_presupuestos.txt", "w") as archivo:
                    for p in presupuestos_registrados:
                        archivo.write(f"Cliente: {p.cliente.nombre} - Telefono: {p.cliente.telefono} - Presupuesto: {p.total} - Estado: {p.estado} - Saldo: {p.finanzas.saldo_pendiente } - Fecha: {p.fecha}\n")
                        
                break # Rompemos el for porque ya encontramos al cliente y no necesitamos seguir buscando
        if not cliente_encontrado:
            print(f"No se encontró un cliente con el nombre {nombre_buscado}.")
            
    elif opcion == "5":
        nombre_buscado = input("Ingrese el nombre del cliente para actualizar el estado del trabajo: ")
        cliente_encontrado = False
        
        for presu in presupuestos_registrados:
            if presu.cliente.nombre == nombre_buscado:
                cliente_encontrado = True
                print(f"Estado actual de {nombre_buscado}: {presu.estado}")
                nuevo_estado = input("Ingrese el nuevo estado del trabajo (Pendiente, En Proceso, Completado): ")
                presu.actualizar_estado(nuevo_estado)
                
                print(f"Estado actualizado. Nuevo estado: {presu.estado}")
                
                # Sobreescribimos el historial para reflejar el nuevo estado
                with open("historial_presupuestos.txt", "w") as archivo:
                    for p in presupuestos_registrados:
                        archivo.write(f"Cliente: {p.cliente.nombre} - Telefono: {p.cliente.telefono} - Presupuesto: {p.total} - Estado: {p.estado} - Saldo: {p.finanzas.saldo_pendiente } - Fecha: {p.fecha}\n")
                        
                break
        if not cliente_encontrado:
            print(f"No se encontró un cliente con el nombre {nombre_buscado}.")
        
        input("\nPresione ENTER para volver al menú principal...")
        
    elif opcion == "6":
        nombre_buscado = input("Ingrese el nombre del cliente para eliminar su presupuesto: ")
        cliente_encontrado = False
        
        for presu in presupuestos_registrados:
            if presu.cliente.nombre == nombre_buscado:
                cliente_encontrado = True
                presupuestos_registrados.remove(presu)
                print(f"Presupuesto de {nombre_buscado} eliminado.")
                
                # Sobreescribimos el historial para reflejar la eliminación
                with open("historial_presupuestos.txt", "w") as archivo:
                    for p in presupuestos_registrados:
                        archivo.write(f"Cliente: {p.cliente.nombre} - Telefono: {p.cliente.telefono} - Presupuesto: {p.total} - Estado: {p.estado} - Saldo: {p.finanzas.saldo_pendiente } - Fecha: {p.fecha}\n")
                        
                break
        if not cliente_encontrado:
            print(f"No se encontró un cliente con el nombre {nombre_buscado}.")
        
        input("\nPresione ENTER para volver al menú principal...")
                
    elif opcion == "7":
        print("Cerrando el sistema. ¡Hasta luego!")
        break
    else:
        print("Opción no válida. Por favor, intente nuevamente.")