from flask_bcrypt import Bcrypt
from flask_bcrypt import check_password_hash

bcrypt = Bcrypt()  # Instancia Bcrypt

# Durante el registro
contrasena = "123"
contrasena_hash = bcrypt.generate_password_hash(contrasena).decode('utf-8')
# Ahora almacena 'contrasena_hash' en la base de datos



# Durante el inicio de sesión
contrasena_proporcionada = "123"
# Recupera la contraseña hash almacenada en la base de datos

if check_password_hash(contrasena_hash, contrasena_proporcionada):
    # La contraseña es correcta
    # Continúa con el inicio de sesión
    print(contrasena_hash)
    print(contrasena_proporcionada)
    print("Contraseña correcta")
else:
    # La contraseña es incorrecta
    # Informa al usuario y maneja el error
    
    print("Contraseña incorrecta")
