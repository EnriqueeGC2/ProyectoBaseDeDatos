import pyodbc

def conectar_bd():
    try:
        conexion = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=DESKTOP-BOOC5R2;DATABASE=TiendaOnline;Trusted_Connection=yes;')
        print("Conexión exitosa")
        return conexion
    except pyodbc.Error as ex:
        print("Error de pyodbc:", ex)
        return None

def ejecutar_consulta(query):
    conexion = conectar_bd()
    if conexion:
        try:
            with conexion:
                cursor = conexion.cursor()
                cursor.execute(query)
                resultados = cursor.fetchall()
                return resultados
        except pyodbc.Error as ex:
            print("Error al ejecutar la consulta:", ex)
            return None
        finally:
            conexion.close()
    else:
        return None
    