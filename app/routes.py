from app import app, render_template
from config import ejecutar_consulta

@app.route('/')
def index():
    query = "SELECT * FROM dbo.Productos;"
    productos = ejecutar_consulta(query)
    return render_template('index.html', productos=productos)
