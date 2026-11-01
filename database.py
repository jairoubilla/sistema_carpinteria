import psycopg2

def conectar_db():
    # Establecemos la conexion con el servidor postgreSQL
    conexion = psycopg2.connect(
        host= "localhost",
        database= "carpinteria_db",
        user= "postgres",
        password= "admin123"
    )
    return conexion

def guardar_en_postgres(presu):
    conexion = conectar_db()
    cursor = conexion.cursor()
    
    # Consulta SQL para insertar datos
    sql = """
        INSERT INTO presupuestos (id_orden, cliente_nombre, cliente_telefono, monto_total, estado, saldo_pendiente, fecha)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    
    valores = (
        presu.id_orden,
        presu.cliente.nombre,
        presu.cliente.telefono,
        presu.total,
        presu.estado,
        presu.finanzas.saldo_pendiente,
        presu.fecha
    )
    
    cursor.execute(sql, valores)
    conexion.commit() # Guardamos los cambios en el servidor
    
    cursor.close()
    conexion.close()
    
def actualizar_estado_en_postgres(presu):
    conexion = conectar_db()
    cursor = conexion.cursor()
    
    # Consulta SQL para actualizar datos
    sql = "UPDATE presupuestos SET estado = %s WHERE id_orden = %s"
    cursor.execute(sql, (presu.estado, presu.id_orden))
    conexion.commit() # Guardamos los cambios en el servidor
    
    cursor.close()
    conexion.close()
    
def actualizar_pago_en_postgres(presu):
    conexion = conectar_db()
    cursor = conexion.cursor()
    
    # Consulta SQL para actualizar datos
    sql = "UPDATE presupuestos SET saldo_pendiente = %s WHERE id_orden = %s"
    cursor.execute(sql, (presu.finanzas.saldo_pendiente, presu.id_orden))
    conexion.commit() # Guardamos los cambios en el servidor
    
    cursor.close()
    conexion.close()
    
def eliminar_en_postgres(presu):
    conexion = conectar_db()
    cursor = conexion.cursor()
    
    # Consulta SQL para eliminar datos
    sql = "DELETE FROM presupuestos WHERE id_orden = %s"
    cursor.execute(sql, (presu.id_orden,))
    conexion.commit() # Guardamos los cambios en el servidor
    
    cursor.close()
    conexion.close()