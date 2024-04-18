from flask import Flask, render_template

app = Flask(__name__)

# Configuración de la aplicación
app.config['SECRET_KEY'] = 'tu_clave_secreta'  # Cambia 'tu_clave_secreta' por una clave segura

# Importa las rutas y los modelos
from app import routes, models
