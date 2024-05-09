from app import app, render_template
from flask import request, redirect, url_for, session
from flask_bcrypt import Bcrypt
from flask_bcrypt import check_password_hash

#from werkzeug.security import generate_password_hash, check_password_hash

from config import ejecutar_consulta

bcrypt = Bcrypt()

@app.route('/')
def index():
    queryCategorias = "SELECT * FROM dbo.CATEGORIAS;"
    categorias = ejecutar_consulta(queryCategorias)

    queryProductos = "SELECT * FROM dbo.PRODUCTOS;"
    productos = ejecutar_consulta(queryProductos)
    return render_template('index.html', categorias=categorias, productos=productos)

@app.route('/productos')
def productos():
    queryProductos = "SELECT * FROM dbo.PRODUCTOS;"
    productos = ejecutar_consulta(queryProductos)
    return render_template('productos.html', productos=productos)

@app.route('/productos_electronicos')
def productosElectronicos():
    queryProductos = "SELECT * FROM dbo.PRODUCTOS WHERE CATEGORIA_ID = 1;"
    productos = ejecutar_consulta(queryProductos)
    return render_template('productosElectronicos.html', productos=productos)

@app.route('/inicio_sesion', methods=['GET', 'POST'])
def inicioSesion():
    if request.method == 'POST':
        correo_electronico = request.form['correo_electronico']
        contrasena = request.form['contrasena']

        # Buscar al usuario en la base de datos por su correo electrónico
        query = "SELECT * FROM usuario WHERE correo_electronico = ?"
        resultado = ejecutar_consulta(query, (correo_electronico,))

        if resultado:
            usuario = resultado[0]  # Tomamos el primer resultado de la lista
            # Verificar si la contraseña es correcta
            if check_password_hash(usuario['contrasena'].strip(), contrasena): #.strip() elimina los espacios en blanco
                # Iniciar sesión y redirigir al usuario a una página protegida
                session['usuario'] = usuario
                return redirect(url_for('pagina_protegida'))
            else:
                return "La contraseña es incorrecta. Por favor, inténtalo de nuevo."
        else:
            return "El correo electrónico no está registrado. Por favor, regístrate primero."

    return render_template('iniciarSesion.html')

@app.route('/pagina-protegida')
def pagina_protegida():
    # Verificar si el usuario está autenticado antes de acceder a esta página
    if 'usuario' in session:
        return "¡Bienvenido a la página protegida!"
    else:
        return redirect(url_for('inicioSesion'))

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        correo_electronico = request.form['correo_electronico']
        contrasena = request.form['contrasena']
        confirmar_contrasena = request.form['confirmar_contrasena']

        # Verificar si las contraseñas coinciden
        if contrasena != confirmar_contrasena:
            return "Las contraseñas no coinciden. Por favor, inténtalo de nuevo."

        # Generar el hash de la contraseña
        contrasena_segura = bcrypt.generate_password_hash(contrasena).decode('utf-8')

        # Verificar si el correo electrónico ya está registrado
        query = "SELECT * FROM usuario WHERE correo_electronico = ?"
        resultado = ejecutar_consulta(query, (correo_electronico,))
        if resultado:
            return "El correo electrónico ya está registrado. Por favor, utiliza otro."
        
        # Insertar el nuevo usuario en la base de datos
        query_insert = "INSERT INTO Usuario (nombre, apellido, correo_electronico, contrasena) VALUES (?, ?, ?, ?)"
        ejecutar_consulta(query_insert, (nombre, apellido, correo_electronico, contrasena_segura), fetch_results=False)
        
        return redirect(url_for('inicioSesion'))  # Redirigir al usuario al inicio de sesión después del registro
    return render_template('registro.html')

