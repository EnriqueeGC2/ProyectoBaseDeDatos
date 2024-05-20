import pyodbc

def conectar_bd():
    try:
        conexion = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=DESKTOP-BOOC5R2;DATABASE=TIENDAENLINEA;Trusted_Connection=yes;')
        print("Conexión exitosa")
        return conexion
    except pyodbc.Error as ex:
        print("Error de pyodbc:", ex)
        return None

def ejecutar_consulta(query, args=None, fetch_results=True):
    conexion = conectar_bd()
    if conexion:
        try:
            with conexion:
                cursor = conexion.cursor()
                if args:
                    cursor.execute(query, args)
                else:
                    cursor.execute(query)
                if fetch_results:
                    columnas = [column[0] for column in cursor.description]
                    resultados = [dict(zip(columnas, fila)) for fila in cursor.fetchall()]
                    return resultados
                else:
                    return None  # No necesitas retornar resultados si no estás esperando resultados
        except pyodbc.Error as ex:
            print("Error al ejecutar la consulta:", ex)
            return None
        finally:
            conexion.close()
    else:
        return None

""" import pymysql

host = 'localhost' 
user = ''
password = ''
db = 'tiendaenlinea'

def conectar_bd():
    try:
        conexion = pymysql.connect(host=host, user=user, password=password, db=db)
        print("Conexión exitosa")
        return conexion
    except pymysql.Error as ex:
        print("Error de pymysql:", ex)
        return None

def ejecutar_consulta(query, args=None, fetch_results=True):
    conexion = conectar_bd()
    if conexion:
        try:
            with conexion.cursor() as cursor:
                if args:
                    cursor.execute(query, args)
                else:
                    cursor.execute(query)
                if fetch_results:
                    columnas = [column[0] for column in cursor.description]
                    resultados = [dict(zip(columnas, fila)) for fila in cursor.fetchall()]
                    return resultados
                else:
                    conexion.commit()
                    return None  # No necesitas retornar resultados si no estás esperando resultados
        except pymysql.Error as ex:
            print("Error al ejecutar la consulta:", ex)
            return None
        finally:
            conexion.close()
    else:
        return None

# Prueba
query = "SELECT * FROM tiendaenlinea.empleados;"
resultados = ejecutar_consulta("SELECT * FROM empleados;")
print(resultados) """