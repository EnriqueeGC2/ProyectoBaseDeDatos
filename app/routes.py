from app import app, render_template
from flask import request, redirect, url_for, session, jsonify
from flask_bcrypt import Bcrypt
from flask_bcrypt import check_password_hash

#from werkzeug.security import generate_password_hash, check_password_hash

from config import ejecutar_consulta

bcrypt = Bcrypt()

@app.route('/')
def index():
    queryCategorias = "SELECT * FROM categorias;"
    categorias = ejecutar_consulta(queryCategorias)

    queryProductos = "SELECT * FROM productos;"
    productos = ejecutar_consulta(queryProductos)
    return render_template('index.html', categorias=categorias, productos=productos)

@app.route('/productos')
def productos():
    queryProductos = "SELECT * FROM productos;"
    productos = ejecutar_consulta(queryProductos)
    return render_template('products/productos.html', productos=productos)

@app.route('/productos_electronicos')
def productosElectronicos():
    queryProductos = "SELECT * FROM productos WHERE subcategoria_id = 1;"
    productos = ejecutar_consulta(queryProductos)
    return render_template('products/productosElectronicos.html', productos=productos)

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        correo_electronico = request.form['correo_electronico']
        contrasena = request.form['contrasena']
        confirmar_contrasena = request.form['confirmar_contrasena']
        primer_nombre = request.form['primer_nombre']
        primer_apellido = request.form['primer_apellido']

        # Verificar si las contraseñas coinciden
        if contrasena != confirmar_contrasena:
            return "Las contraseñas no coinciden. Por favor, inténtalo de nuevo."

        # Generar el hash de la contraseña
        contrasena_segura = bcrypt.generate_password_hash(contrasena).decode('utf-8')

        # Verificar si el nombre de usuario ya está registrado
        query = "SELECT * FROM Usuarios WHERE correo_electronico = ?"
        resultado = ejecutar_consulta(query, (correo_electronico,))
        if resultado:
            return "El nombre de usuario ya está registrado. Por favor, utiliza otro."

        # Insertar el nuevo usuario en la tabla Usuarios
        query_insert_usuario = "INSERT INTO Usuarios (correo_electronico, contraseña, rol, primer_nombre, primer_apellido) VALUES (?, ?, ?, ?, ?)"
        ejecutar_consulta(query_insert_usuario, (correo_electronico, contrasena_segura, 'user', primer_nombre, primer_apellido), fetch_results=False)

        # Obtener el ID del nuevo usuario insertado
        query_usuario_id = "SELECT usuario_id FROM Usuarios WHERE correo_electronico = ?"
        nuevo_usuario = ejecutar_consulta(query_usuario_id, (correo_electronico,))
        usuario_id = nuevo_usuario[0]['usuario_id']

        # Insertar los datos del cliente en la tabla Clientes
        query_insert_cliente = """
            INSERT INTO Clientes (usuario_id)
            VALUES (?)
        """
        ejecutar_consulta(query_insert_cliente, (usuario_id), fetch_results=False)

        return redirect(url_for('inicioSesion'))  # Redirigir al usuario al inicio de sesión después del registro

    return render_template('registro.html')

@app.route('/inicio_sesion', methods=['GET', 'POST'])
def inicioSesion():
    mensaje = ''

    if request.method == 'POST':
        correo_electronico = request.form['correo_electronico']
        contrasena = request.form['contrasena']

        # Buscar al usuario en la base de datos por su nombre de usuario
        query = "SELECT * FROM Usuarios WHERE correo_electronico = ?"
        resultado = ejecutar_consulta(query, (correo_electronico,))

        if resultado:
            usuario = resultado[0]  # Tomamos el primer resultado de la lista
            # Verificar si la contraseña es correcta
            if bcrypt.check_password_hash(usuario['contraseña'].strip(), contrasena):  # .strip() elimina los espacios en blanco
                # Iniciar sesión y redirigir al usuario a una página protegida
                session['user'] = usuario
                if usuario['rol'].strip() == 'admin':
                    return redirect(url_for('pagina_protegida_admin'))
                else:
                    return redirect(url_for('pagina_protegida'))
            else:
                mensaje = "La contraseña es incorrecta. Por favor, inténtalo de nuevo."
        else:
            mensaje = "El nombre de usuario no está registrado. Por favor, regístrate primero."
    
    return render_template('iniciarSesion.html', mensaje=mensaje)

@app.route('/pagina-protegida')
def pagina_protegida():
    # Verificar si el usuario está autenticado antes de acceder a esta página
    if 'user' in session:
        #print(session['user']['primer_nombre'])
        usuario_id = session['user']['usuario_id']
        query = "SELECT * FROM dbo.Clientes WHERE usuario_id = ?;"
        cliente = ejecutar_consulta(query, (usuario_id,))
        return render_template('user/indexUsuario.html', nombre=session['user']['primer_nombre'], cliente=cliente[0])
    else:
        return redirect(url_for('inicioSesion'))

@app.route('/cerrar_sesion')
def cerrarSesion():
    # Eliminar el nombre del usuario de la sesión al cerrar sesión
    session.pop('user', None)
    return redirect(url_for('inicioSesion'))

@app.route('/pagina-protegida-admin')
def pagina_protegida_admin():
    # Verificar si el usuario está autenticado antes de acceder a esta página
    if 'user' in session:
        query = "SELECT * FROM Usuarios WHERE rol = 'user'"
        usuarios = ejecutar_consulta(query)
        return render_template('admin/indexAdmin.html', usuarios=usuarios, nombre=session['user']['primer_nombre'])

@app.route('/admin/usuarios/eliminar/<int:usuario_id>', methods=['POST'])
def eliminar_usuario(usuario_id):
    query = "DELETE FROM Usuario WHERE usuario_id = ?"
    ejecutar_consulta(query, (usuario_id,), fetch_results=False)
    return redirect(url_for('pagina_protegida_admin'))

@app.route('/admin/productos')
def editar_productos():
    # Verificar si el usuario está autenticado antes de acceder a esta página
    if 'user' in session:
        query = "SELECT * FROM dbo.PRODUCTOS;"
        productos = ejecutar_consulta(query)
        return render_template('admin/productos.html', productos=productos, nombre=session['user']['primer_nombre'])
    else:
        return redirect(url_for('inicioSesion'))

@app.route('/admin/producto/eliminar/<int:producto_id>', methods=['POST'])
def eliminar_producto(productoID):
    query = "DELETE FROM Productos WHERE producto_id = ?"
    ejecutar_consulta(query, (productoID,), fetch_results=False)
    return redirect(url_for('editar_productos'))

