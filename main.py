from clientes import Cliente
from presupuestos import Presupuesto

import os
import json

clientes_registrados = []
presupuestos_registrados = []

def guardar_datos():
    # Craemos una lista vacia para guardar los datos puros
    lista_para_guardar = []
    
    # Recorremos nuestros objetos y los transformamos en diccionarios
    for presu in presupuestos_registrados:
        diccionario = {
            "cliente": presu.cliente.nombre,
            "telefono": presu.cliente.telefono,
            "monto_total": presu.total,
            "estado": presu.estado,
            "saldo_pendiente": presu.finanzas.saldo_pendiente,
            "fecha": presu.fecha
        }
        lista_para_guardar.append(diccionario)
        
    # Guardamos la lista de diccionarios en un archivo .json mágico
    with open("base_datos.json", "w") as archivo:
        json.dump(lista_para_guardar, archivo, indent=4)
        

# --- RUTINA DE ARRANQUE ---
try:
    with open("base_datos.json", "r") as archivo:
        # json.load lee el archivo y nos devuelve la lista ya armada
        datos_guardados = json.load(archivo)
        
        for dato in datos_guardados:
            # 1. Reconstruimos los objetos usando las claves del diccionario
            cliente_recuperado = Cliente(dato["cliente"], dato["telefono"])
            presu_recuperado = Presupuesto(cliente_recuperado, dato["monto_total"])
            
            # 2. Inyectamos la historia
            presu_recuperado.estado = dato["estado"]
            presu_recuperado.finanzas.saldo_pendiente = dato["saldo_pendiente"]
            presu_recuperado.fecha = dato["fecha"]
            
            # 3. Guardamos en la memoria RAM
            clientes_registrados.append(cliente_recuperado)
            presupuestos_registrados.append(presu_recuperado)
            
    print(f"SISTEMA INICIADO: Se recuperaron {len(presupuestos_registrados)} presupuestos (Formato JSON).")
except FileNotFoundError:
    print("SISTEMA INICIADO: Base de datos JSON limpia. No se encontraron registros.")
    

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
        
        guardar_datos()
        
    elif opcion == "2":
        print("\n--- PANEL DE REPORTES ---")
        print("A. Ver TODOS los presupuestos")
        print("B. Ver trabajos ACTIVOS (Pendientes / En Proceso)")
        
        filtro = input("Seleccione un filtro (A/B): ").strip().upper()
        
        print("\n---  LISTADO DE PRESUPUESTOS ---")
        for presu in presupuestos_registrados:
            estado_limpio = presu.estado.strip().lower()
            
            if filtro == "B" and estado_limpio in ["entregado", "terminado", "completado"]:
                continue # Saltamos los presupuestos que no están activos
            
            print(f"Fecha: {presu.fecha} - Presupuesto: {presu.total} - Cliente: {presu.cliente.nombre} - Estado: {presu.estado}")
            
        input("\nPresione ENTER para volver al menú principal...")
        
    elif opcion == "3":
        try:
            with open("base_datos.json", "r") as archivo:
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
                
                guardar_datos()
                        
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
                
                guardar_datos()
                        
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
                
                guardar_datos()
                        
                break
        if not cliente_encontrado:
            print(f"No se encontró un cliente con el nombre {nombre_buscado}.")
        
        input("\nPresione ENTER para volver al menú principal...")
                
    elif opcion == "7":
        print("Cerrando el sistema. ¡Hasta luego!")
        break
    else:
        print("Opción no válida. Por favor, intente nuevamente.")