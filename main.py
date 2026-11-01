from clientes import Cliente
from presupuestos import Presupuesto
from database import conectar_db, guardar_en_postgres, actualizar_estado_en_postgres, actualizar_pago_en_postgres, eliminar_en_postgres

import os
import json
import subprocess


def limpiar_pantalla():
    if os.name == "nt":
        subprocess.run(["cmd", "/c", "cls"], shell=False, check=False,
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    else:
        subprocess.run(["clear"], shell=False, check=False,
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# --- RUTINA DE ARRANQUE ---

clientes_registrados = []
presupuestos_registrados = []

try:
    conexion = conectar_db()
    cursor = conexion.cursor()
    
    # Pedimos todos los registros de nuestra tabla en PostgreSQL
    cursor.execute("SELECT id_orden, cliente_nombre, cliente_telefono, monto_total, estado, saldo_pendiente, fecha FROM presupuestos")
    filas = cursor.fetchall()
    
    for fila in filas:
        # Extraemos los datos según el orden de las columnas en el SELECT
        id_orden_db, nombre_db, telefono_db, monto_db, estado_db, saldo_db, fecha_db = fila
        
        # Reconstruimos los objetos
        cliente_recuperado = Cliente(nombre_db, telefono_db)
        presu_recuperado = Presupuesto(cliente_recuperado, float(monto_db), id_orden_db)
        
        presu_recuperado.estado = estado_db
        presu_recuperado.finanzas.saldo_pendiente = float(saldo_db)
        presu_recuperado.fecha = fecha_db
        
        clientes_registrados.append(cliente_recuperado)
        presupuestos_registrados.append(presu_recuperado)
        
    cursor.close()
    conexion.close()
    print(f"SISTEMA INICIADO: Se recuperaron {len(presupuestos_registrados)} presupuestos desde PostgreSQL.")
    
except Exception as e:
    print(f"SISTEMA INICIADO: Error al conectar con la base de datos o tabla vacía. ({e})")

# --- MENU PRINCIPAL ---
# Extraemos los datos segun el orden de las columnas en el SELECT

while True:
    limpiar_pantalla()
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
        
        # Guardamos en la base de datos
        guardar_en_postgres(nuevo_presupuesto)
        print("¡Presupuesto guardado exitosamente en PostgreSQL!")
        
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
            
            print(f"[Orden #{presu.id_orden}] Fecha: {presu.fecha} - Presupuesto: {presu.total} - Cliente: {presu.cliente.nombre} - Estado: {presu.estado}")
            
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
        try:
            id_buscado = int(input("Ingrese el NÚMERO DE ORDEN para registrar un pago: "))
        except ValueError:
            print("ERROR: Debe ingresar un número válido.")
            input("\nPresione ENTER para volver al menú principal...")
            continue
        
        orden_encontrada = False
        
        for presu in presupuestos_registrados:
            # Comparamos la clave primaria
            if presu.id_orden == id_buscado:
                orden_encontrada = True
                print(f"Cliente: {presu.cliente.nombre} | Saldo actual: ${presu.finanzas.saldo_pendiente}")
                
                # Pedimos el dinero con nuestro blindaje
                while True:
                    try:
                        monto_pago = float(input("Ingrese el monto del pago: "))
                        break
                    except ValueError:
                        print("ERROR: Ingrese un número válido para el monto.")
                
                presu.finanzas.registrar_pago(monto_pago)
                print(f"Pago registrado. Nuevo saldo: ${presu.finanzas.saldo_pendiente}")
                
                actualizar_pago_en_postgres(presu)  # Guardamos el cambio en la base de datos
                break
                
        if not orden_encontrada:
            print(f"No se encontró ninguna orden con el número #{id_buscado}.")
            
        input("\nPresione ENTER para volver al menú principal...")
        
    elif opcion == "5":
        # Usamos un try/except por si el usuario tipea letras en lugar del número de orden
        try:
            id_buscado = int(input("Ingrese el NÚMERO DE ORDEN para actualizar el estado: "))
        except ValueError:
            print("ERROR: Debe ingresar un número válido.")
            input("\nPresione ENTER para volver al menú principal...")
            continue # Salta de vuelta al inicio del menú
        
        orden_encontrada = False
        
        for presu in presupuestos_registrados:
            # Comparamos los IDs 
            if presu.id_orden == id_buscado:
                orden_encontrada = True
                print(f"Trabajo de: {presu.cliente.nombre} | Estado actual: {presu.estado}")
                
                nuevo_estado = input("Ingrese el nuevo estado del trabajo: ")
                presu.actualizar_estado(nuevo_estado)
                
                print(f"Estado actualizado con éxito a: {presu.estado}")
                
                # Función de guardado
                actualizar_estado_en_postgres(presu)  # Guardamos el cambio en la base de datos
                break
            
        if not orden_encontrada:
            print(f"No se encontró ninguna orden con el número #{id_buscado}.")
            
        input("\nPresione ENTER para volver al menú principal...")    
        
    elif opcion == "6":
        try:
            id_buscado = int(input("Ingrese el NÚMERO DE ORDEN para eliminar su presupuesto: "))
        except ValueError:
            print("ERROR: Debe ingresar un número válido.")
            input("\nPresione ENTER para volver al menú principal...")
            continue
        
        orden_encontrada = False
        
        for presu in presupuestos_registrados:
            if presu.id_orden == id_buscado:
                orden_encontrada = True
                
                # Borramos el objeto de la lista RAM
                presupuestos_registrados.remove(presu)
                print(f"¡La orden #{id_buscado} ha sido eliminada definitivamente!")
                
                eliminar_en_postgres(presu)  # Guardamos el cambio en la base de datos
                break
            
        if not orden_encontrada:
            print(f"No se encontró ninguna orden con el número #{id_buscado}.")
            
        input("\nPresione ENTER para volver al menú principal...")
                
    elif opcion == "7":
        print("Cerrando el sistema. ¡Hasta luego!")
        break
    else:
        print("Opción no válida. Por favor, intente nuevamente.")