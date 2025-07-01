from flask import Flask, render_template, request
import sqlite3
import os  # <-- necesario para leer la variable de entorno PORT

app = Flask(__name__)

def obtener_datos(filtro):
    conn = sqlite3.connect("base_datos.db")
    cursor = conn.cursor()
    query = """
        SELECT * FROM mi_tabla
        WHERE nombre LIKE ? OR apellido LIKE ?
    """
    like_filtro = f"%{filtro}%"
    cursor.execute(query, (like_filtro, like_filtro))
    resultados = cursor.fetchall()
    columnas = [desc[0] for desc in cursor.description]
    conn.close()
    return resultados, columnas

@app.route('/', methods=['GET', 'POST'])
def index():
    resultados = []
    columnas = []
    if request.method == 'POST':
        filtro = request.form['filtro']
        resultados, columnas = obtener_datos(filtro)
    return render_template('index.html', resultados=resultados, columnas=columnas)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Usa el puerto asignado por Render o 5000 localmente
    app.run(host='0.0.0.0', port=port)