from app import app, render_template
from flask import request, redirect, url_for, session, jsonify
from flask_bcrypt import Bcrypt
from flask_bcrypt import check_password_hash
from datetime import datetime

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
        # Seleccionar todos los usuarios que no sean administradores y sus datos de Clientes
        query = """
        SELECT Usuarios.usuario_id, Usuarios.primer_nombre, Usuarios.primer_apellido, Usuarios.correo_electronico, 
               Clientes.segundo_nombre, Clientes.segundo_apellido, Clientes.numero_telefono, Clientes.dpi, Clientes.direccion
        FROM Usuarios
        LEFT JOIN Clientes ON Usuarios.usuario_id = Clientes.usuario_id
        WHERE Usuarios.rol = 'user'
        """
        usuarios_clientes = ejecutar_consulta(query)
        
        return render_template('admin/indexAdmin.html', usuarios_clientes=usuarios_clientes, nombre=session['user']['primer_nombre'])
    else:
        return redirect(url_for('login'))  # Redirigir a login si el usuario no está en sesión

@app.route('/admin/usuarios/eliminar/<int:usuario_id>', methods=['POST'])
def eliminar_usuario(usuario_id):
    # Eliminar al usuario de la base de datos
    query = "DELETE FROM Usuarios WHERE usuario_id = ?"
    ejecutar_consulta(query, (usuario_id,), fetch_results=False)
    # Eliminar al cliente de la base de datos
    query = "DELETE FROM Clientes WHERE usuario_id = ?"
    ejecutar_consulta(query, (usuario_id,), fetch_results=False)
    return redirect(url_for('pagina_protegida_admin'))

@app.route('/admin/usuarios/agregar-informacion', methods=['POST'])
def agregar_info_cliente():
    if 'user' in session:
        usuario_id = session['user']['usuario_id']
        segundo_nombre = request.form['segundo_nombre']
        segundo_apellido = request.form['segundo_apellido']
        direccion = request.form['direccion']
        numero_telefono = request.form['numero_telefono']
        dpi = request.form['dpi']

        query = """
        UPDATE Clientes
        SET segundo_nombre = ?, segundo_apellido = ?, direccion = ?, numero_telefono = ?, dpi = ?
        WHERE usuario_id = ?
        """
        ejecutar_consulta(query, (segundo_nombre, segundo_apellido, direccion, numero_telefono, dpi, usuario_id), fetch_results=False)
        return redirect(url_for('pagina_protegida'))
    else:
        return redirect(url_for('login'))  # Redirigir a login si el usuario no está en sesión

@app.route('/admin/productos')
def editar_productos():
    # Verificar si el usuario está autenticado antes de acceder a esta página
    if 'user' in session:
        # Obtener todos los productos de la base de datos
        query = "SELECT * FROM dbo.PRODUCTOS;"
        productos = ejecutar_consulta(query)

        # Obtener todas las subcategorías de la base de datos
        query_subcategorias = "SELECT * FROM dbo.SUBCATEGORIAS;"
        subcategorias = ejecutar_consulta(query_subcategorias)
        return render_template('admin/productos.html', productos=productos, subcategorias=subcategorias, nombre=session['user']['primer_nombre'])
    else:
        return redirect(url_for('inicioSesion'))

@app.route('/admin/producto/eliminar/<int:producto_id>', methods=['POST'])
def eliminar_producto(producto_id):
    query = "DELETE FROM Productos WHERE producto_id = ?"
    ejecutar_consulta(query, (producto_id,), fetch_results=False)
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

# CARRITO Y BOTON DE COMPRAS
@app.route('/agregar_carrito/<int:producto_id>', methods=['POST'])
def agregar_carrito(producto_id):
    usuario_id = session['user']['usuario_id']  # Obtener cliente_id de la sesión
    if not usuario_id:
        return redirect(url_for('inicioSesion'))

    cantidad = int(request.form.get('cantidad', 1))

    # Verificar si el carrito existe para el cliente
    query_carrito = "SELECT carrito_id FROM Carrito WHERE usuario_id = ?"
    carrito = ejecutar_consulta(query_carrito, (usuario_id,))

    if not carrito:
        query_crear_carrito = "INSERT INTO Carrito (usuario_id) OUTPUT INSERTED.carrito_id VALUES (?)"
        carrito_id = ejecutar_consulta(query_crear_carrito, (usuario_id,), fetch_results=True)[0]['carrito_id']
    else:
        carrito_id = carrito[0]['carrito_id']

    # Obtener el precio del producto
    query_producto = "SELECT precio FROM Productos WHERE producto_id = ?"
    producto = ejecutar_consulta(query_producto, (producto_id,))[0]
    precio_unitario = producto['precio']

    # Insertar producto en el carrito
    query_detalle = """
    INSERT INTO DetallesCarrito (carrito_id, producto_id, cantidad, precio_unitario)
    VALUES (?, ?, ?, ?)
    """
    ejecutar_consulta(query_detalle, (carrito_id, producto_id, cantidad, precio_unitario), fetch_results=False)

    return redirect(url_for('ver_carrito'))

@app.route('/carrito')
def ver_carrito():
    usuario_id = session['user']['usuario_id']  # Suponiendo que el cliente está en la sesión
    query_carrito = """
    SELECT dc.producto_id, p.nombre_producto, dc.cantidad, dc.precio_unitario, p.url_imagen,
           (dc.cantidad * dc.precio_unitario) AS total
    FROM Carrito c
    JOIN DetallesCarrito dc ON c.carrito_id = dc.carrito_id
    JOIN Productos p ON dc.producto_id = p.producto_id
    WHERE c.usuario_id = ?
    """
    items_carrito = ejecutar_consulta(query_carrito, (usuario_id,))
    total = sum(item['total'] for item in items_carrito) if items_carrito else 0
    
    return render_template('products/carrito.html', items_carrito=items_carrito, total=total)

# Ruta para actualizar la cantidad de un producto en el carrito
@app.route('/actualizar_carrito/<int:producto_id>', methods=['POST'])
def actualizar_carrito(producto_id):
    usuario_id = session['user']['usuario_id']  # Suponiendo que el cliente está en la sesión
    nueva_cantidad = int(request.form.get('cantidad'))
    
    query_carrito = "SELECT carrito_id FROM Carrito WHERE usuario_id = ?"
    carrito = ejecutar_consulta(query_carrito, (usuario_id,))
    carrito_id = carrito[0]['carrito_id']
    
    query_actualizar = """
    UPDATE DetallesCarrito
    SET cantidad = ?
    WHERE carrito_id = ? AND producto_id = ?
    """
    ejecutar_consulta(query_actualizar, (nueva_cantidad, carrito_id, producto_id), fetch_results=False)
    
    return redirect(url_for('ver_carrito'))

@app.route('/eliminar_carrito/<int:producto_id>', methods=['POST'])
def eliminar_carrito(producto_id):
    usuario_id = session['user']['usuario_id']
    if not usuario_id:
        return redirect(url_for('inicioSesion'))

    query_carrito = "SELECT carrito_id FROM Carrito WHERE usuario_id = ?"
    carrito = ejecutar_consulta(query_carrito, (usuario_id,))
    if not carrito:
        return redirect(url_for('ver_carrito'))

    carrito_id = carrito[0]['carrito_id']

    query_eliminar = "DELETE FROM DetallesCarrito WHERE carrito_id = ? AND producto_id = ?"
    ejecutar_consulta(query_eliminar, (carrito_id, producto_id), fetch_results=False)

    return redirect(url_for('ver_carrito'))

@app.route('/comprar', methods=['POST'])
def comprar():
    usuario_id = session['user']['usuario_id']
    if not usuario_id:
        return redirect(url_for('inicioSesion'))

    # Obtener el cliente_id a partir del usuario_id
    query_cliente = "SELECT cliente_id FROM Clientes WHERE usuario_id = ?"
    cliente = ejecutar_consulta(query_cliente, (usuario_id,))
    if not cliente:
        print("Cliente no encontrado para usuario_id:", usuario_id)  # Depuración
        return redirect(url_for('ver_carrito'))

    cliente_id = cliente[0]['cliente_id']
    print("Cliente ID:", cliente_id)  # Depuración

    # Obtener los productos en el carrito
    query_carrito = """
    SELECT dc.producto_id, dc.cantidad, dc.precio_unitario
    FROM Carrito c
    JOIN DetallesCarrito dc ON c.carrito_id = dc.carrito_id
    WHERE c.usuario_id = ?
    """
    items_carrito = ejecutar_consulta(query_carrito, (cliente_id,))
    if not items_carrito:
        print("No se encontraron productos en el carrito para cliente_id:", cliente_id)  # Depuración
        return redirect(url_for('ver_carrito'))

    # Calcular el total de la venta
    total_venta = sum(item['cantidad'] * item['precio_unitario'] for item in items_carrito)

    # Insertar la venta en la tabla Ventas
    query_venta = "INSERT INTO Ventas (cliente_id, fecha_venta, total_venta) OUTPUT INSERTED.venta_id VALUES (?, GETDATE(), ?)"
    venta = ejecutar_consulta(query_venta, (cliente_id, total_venta), fetch_results=True)
    if not venta:
        print("Error al insertar la venta para cliente_id:", cliente_id)  # Depuración
        return redirect(url_for('ver_carrito'))

    venta_id = venta[0]['venta_id']

    # Insertar los detalles de la venta
    query_detalles_venta = """
    INSERT INTO DetallesVenta (venta_id, producto_id, cantidad, precio_unitario)
    VALUES (?, ?, ?, ?)
    """
    for item in items_carrito:
        ejecutar_consulta(query_detalles_venta, (venta_id, item['producto_id'], item['cantidad'], item['precio_unitario']), fetch_results=False)

    # Insertar la factura
    query_factura = "INSERT INTO Facturas (venta_id, fecha_factura, total) VALUES (?, GETDATE(), ?)"
    ejecutar_consulta(query_factura, (venta_id, total_venta), fetch_results=False)

    # Vaciar el carrito
    query_vaciar_carrito = "DELETE FROM DetallesCarrito WHERE carrito_id = (SELECT carrito_id FROM Carrito WHERE usuario_id = ?)"
    ejecutar_consulta(query_vaciar_carrito, (usuario_id,), fetch_results=False)

    return redirect(url_for('ver_carrito'))

# Auditorias
@app.route('/auditorias')
def auditorias():
    if 'user' in session:
        query = "SELECT * FROM Auditoria;"
        auditorias = ejecutar_consulta(query)
        return render_template('admin/auditorias/auditoriaPrincipal.html', auditorias=auditorias, nombre=session['user']['primer_nombre'])
    else:
        return redirect(url_for('inicioSesion'))
    
# Reporte Diario de Auditorias    
@app.route('/auditorias/reporte-diario')
def reporte_diario():
    if 'user' in session:
        query = """
        SELECT 
            AuditID, EventType, ObjectName, ObjectSchema, ExecutedBy, ExecutionDate, OldValue, NewValue
        FROM 
            [dbo].[Auditoria]
        WHERE 
            CAST(ExecutionDate AS DATE) = CAST(GETDATE() AS DATE)
        ORDER BY 
            ExecutionDate DESC;
        """
        auditorias = ejecutar_consulta(query)
        return render_template('admin/auditorias/reporteDiario.html', auditorias=auditorias, nombre=session['user']['primer_nombre'])
    else:
        return redirect(url_for('inicioSesion'))
    
# Reporte Semanal de Auditorias
@app.route('/auditorias/reporte-semanal')
def reporte_semanal():
    if 'user' in session:
        query = """
        SELECT 
            AuditID, EventType, ObjectName, ObjectSchema, ExecutedBy, ExecutionDate, OldValue, NewValue
        FROM 
            [dbo].[Auditoria]
        WHERE 
            DATEPART(WEEK, ExecutionDate) = DATEPART(WEEK, GETDATE())
        ORDER BY 
            ExecutionDate DESC;
        """
        auditorias = ejecutar_consulta(query)
        return render_template('admin/auditorias/reporteSemanal.html', auditorias=auditorias, nombre=session['user']['primer_nombre'])
    else:
        return redirect(url_for('inicioSesion'))
    
# Reporte Cambios por usuario auditoria
@app.route('/auditorias/reporte-usuario', methods=['GET', 'POST']) 
def reporte_usuario():
    if 'user' in session:
        total_query = """
        SELECT 
            ExecutedBy, COUNT(*) AS ChangeCount
        FROM 
            [dbo].[Auditoria]
        GROUP BY 
            ExecutedBy
        ORDER BY 
            ChangeCount DESC;
        """
        total_auditorias = ejecutar_consulta(total_query)

        user_auditorias = None
        if request.method == 'POST' and 'nombre' in request.form:
            nombre = request.form['nombre']
            user_query = """
            SELECT 
                AuditID, EventType, ObjectName, ObjectSchema, ExecutedBy, ExecutionDate, OldValue, NewValue
            FROM 
                [dbo].[Auditoria]
            WHERE 
                ExecutedBy = ?
            ORDER BY 
                ExecutionDate DESC;
            """
            user_auditorias = ejecutar_consulta(user_query, nombre)
        
        return render_template('admin/auditorias/reporteUsuario.html', 
                               total_auditorias=total_auditorias, 
                               user_auditorias=user_auditorias, 
                               nombre=session['user']['primer_nombre'])
    else:
        return redirect(url_for('inicioSesion'))

# Reporte Cambios por eventos auditoria
@app.route('/auditorias/reporte-eventos', methods=['GET', 'POST']) 
def reporte_eventos():
    if 'user' in session:
        total_query = """
        SELECT 
            EventType, COUNT(*) AS EventCount
        FROM 
            [dbo].[Auditoria]
        GROUP BY 
            EventType 
        ORDER BY 
            EventCount DESC;
        """
        total_auditorias = ejecutar_consulta(total_query)

        user_auditorias = None
        if request.method == 'POST' and 'nombre' in request.form:
            nombre = request.form['nombre']
            user_query = """
            SELECT 
                AuditID, EventType, ObjectName, ObjectSchema, ExecutedBy, ExecutionDate, OldValue, NewValue
            FROM 
                [dbo].[Auditoria]
            WHERE 
                EventType = ?
            ORDER BY 
                ExecutionDate DESC;
            """
            user_auditorias = ejecutar_consulta(user_query, nombre)
        
        return render_template('admin/auditorias/reporteEvento.html', 
                               total_auditorias=total_auditorias, 
                               user_auditorias=user_auditorias, 
                               nombre=session['user']['primer_nombre'])
    else:
        return redirect(url_for('inicioSesion'))
    
# Reporte Cambios por objeto especifico auditoria
@app.route('/auditorias/reporte-objetos', methods=['GET', 'POST'])
def reporte_objetos():
    if 'user' in session:
        total_query = """
        SELECT 
            ObjectName, COUNT(*) AS ObjectCount
        FROM 
            [dbo].[Auditoria]
        GROUP BY 
            ObjectName
        ORDER BY 
            ObjectCount DESC;
        """
        total_auditorias = ejecutar_consulta(total_query)

        user_auditorias = None
        if request.method == 'POST' and 'nombre' in request.form:
            nombre = request.form['nombre']
            user_query = """
            SELECT 
                AuditID, EventType, ObjectName, ObjectSchema, ExecutedBy, ExecutionDate, OldValue, NewValue
            FROM 
                [dbo].[Auditoria]
            WHERE 
                ObjectName = ?
            ORDER BY 
                ExecutionDate DESC;
            """
            user_auditorias = ejecutar_consulta(user_query, nombre)
        
        return render_template('admin/auditorias/reporteObjeto.html', 
                               total_auditorias=total_auditorias, 
                               user_auditorias=user_auditorias, 
                               nombre=session['user']['primer_nombre'])
    else:
        return redirect(url_for('inicioSesion'))
    
# Reporte Cambios por fechas auditoria
@app.route('/auditorias/reporte-fechas', methods=['GET', 'POST'])
def reporte_fechas():
    resultados = None
    if request.method == 'POST':
        # Obtener las fechas del formulario
        start_date = request.form['start_date']
        end_date = request.form['end_date']

        # Ejecutar la consulta SQL
        query = """
            SELECT 
                AuditID, EventType, ObjectName, ObjectSchema, ExecutedBy, ExecutionDate, OldValue, NewValue
            FROM 
                [dbo].[Auditoria]
            WHERE 
                ExecutionDate BETWEEN ? AND ?
            ORDER BY 
                ExecutionDate DESC;
        """
        args = (start_date, end_date)
        resultados = ejecutar_consulta(query, args)

    return render_template('admin/auditorias/reporteFechas.html', resultados=resultados)

 