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

@app.route('/productos_electronicos')
def productosElectronicos():
    queryProductos = "SELECT * FROM productos WHERE subcategoria_id = 1 OR subcategoria_id = 2 OR subcategoria_id = 3;"
    productos = ejecutar_consulta(queryProductos)
    return render_template('products/productosElectronicos.html', productos=productos)

@app.route('/productos_hogar')
def productos_hogar():
    queryProductos = "SELECT * FROM productos WHERE subcategoria_id = 13 OR subcategoria_id = 14 OR subcategoria_id = 15;"
    productosHogar = ejecutar_consulta(queryProductos)
    return render_template('products/productosHogar.html', productosHogar=productosHogar)

@app.route('/productos_ropa')
def productos_ropa():
    queryProductos = "SELECT * FROM productos WHERE subcategoria_id = 4 OR subcategoria_id = 5 OR subcategoria_id = 6;"
    productos = ejecutar_consulta(queryProductos)
    return render_template('products/productosRopa.html', productos=productos)

@app.route('/productos_juguetes')
def productos_juguetes():
    queryProductos = "SELECT * FROM productos WHERE subcategoria_id = 7 OR subcategoria_id = 8 OR subcategoria_id = 9;"
    productos = ejecutar_consulta(queryProductos)
    return render_template('products/productosJuguetes.html', productos=productos)

@app.route('/productos_deportes')
def productos_deportes():
    queryProductos = "SELECT * FROM productos WHERE subcategoria_id = 10 OR subcategoria_id = 11 OR subcategoria_id = 12;"
    productos = ejecutar_consulta(queryProductos)
    return render_template('products/productosDeportes.html', productos=productos)

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
        usuario_id = session['user']['usuario_id']
        # Seleccionar todos los usuarios que no sean administradores
        query = "SELECT * FROM Usuarios WHERE rol = 'user'"
        usuarios = ejecutar_consulta(query)
        # Seleccionar todos la informacion de lo clientes
        query = "SELECT * FROM Clientes WHERE usuario_id = ?"
        clientes = ejecutar_consulta(query, (usuario_id,))    
        return render_template('admin/indexAdmin.html', usuarios=usuarios, clientes=clientes,nombre=session['user']['primer_nombre'])

@app.route('/admin/usuarios/eliminar/<int:usuario_id>', methods=['POST'])
def eliminar_usuario(usuario_id):
    # Eliminar al usuario de la base de datos
    query = "DELETE FROM Usuarios WHERE usuario_id = ?"
    ejecutar_consulta(query, (usuario_id,), fetch_results=False)
    # Eliminar al cliente de la base de datos
    query = "DELETE FROM Clientes WHERE usuario_id = ?"
    ejecutar_consulta(query, (usuario_id,), fetch_results=False)
    return redirect(url_for('pagina_protegida_admin'))

@app.route('/admin/productos')
def editar_productos():
    # Verificar si el usuario está autenticado antes de acceder a esta página
    if 'user' in session:
        # Obtener todos los productos de la base de datos
        query = "SELECT * FROM dbo.PRODUCTOS;"
        productos = ejecutar_consulta(query)

        # Obtener todas las categorías de la base de datos
        query_categorias = "SELECT * FROM dbo.CATEGORIAS;"
        categorias = ejecutar_consulta(query_categorias)

        # Obtener todas las subcategorías de la base de datos
        query_subcategorias = "SELECT * FROM dbo.SUBCATEGORIAS;"
        subcategorias = ejecutar_consulta(query_subcategorias)

        return render_template('admin/productos.html', productos=productos, categorias=categorias, subcategorias=subcategorias, nombre=session['user']['primer_nombre'])
    else:
        return redirect(url_for('inicioSesion'))

@app.route('/admin/producto/eliminar/<int:producto_id>', methods=['POST'])
def eliminar_producto(productoID):
    query = "DELETE FROM Productos WHERE producto_id = ?"
    ejecutar_consulta(query, (productoID,), fetch_results=False)
    return redirect(url_for('editar_productos'))

@app.route('/admin/producto/agregar', methods=['POST'])
def agregar_producto():
    nombre = request.form['nombre_producto']
    detalles = request.form['detalles']
    marca = request.form['marca']
    precio = request.form['precio']
    stock = request.form['stock']
    subcategoria_id = request.form['subcategoria_id']
    url_imagen = request.form['url_imagen']

    query = "INSERT INTO Productos (nombre_producto, detalles, marca, precio, stock, subcategoria_id, url_imagen) VALUES (?, ?, ?, ?, ?, ?, ?)"
    ejecutar_consulta(query, (nombre, detalles, marca, precio, stock, subcategoria_id, url_imagen), fetch_results=False)

    return redirect(url_for('editar_productos'))

