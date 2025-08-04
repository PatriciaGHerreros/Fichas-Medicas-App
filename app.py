from flask import Flask, jsonify, render_template, request, redirect, url_for
import sqlite3
app = Flask(__name__)

def obtener_conexion ():
    conexion = sqlite3.connect('fichas.db')
    conexion.row_factory = sqlite3.Row
    return conexion

@app.route('/')
def index():
    conexion = obtener_conexion()
    fichas = conexion.execute('SELECT * FROM ficha WHERE eliminado = 0').fetchall()
    conexion.close()
    return render_template('index.html', fichas=fichas, title="Lista de Fichas Médicas")

@app.route('/pendientes')
def pendientes():
    conexion = obtener_conexion()
    fichas = conexion.execute('SELECT * FROM ficha WHERE done = 0 AND eliminado= 0').fetchall()
    conexion.close()
    return render_template('index.html', fichas=fichas, title="Fichas Pendientes")


@app.route('/atendidas')
def atendidas():
    conexion = obtener_conexion()
    fichas = conexion.execute('SELECT * FROM ficha WHERE done = 1 AND eliminado = 0').fetchall()
    conexion.close()
    return render_template('index.html', fichas=fichas, title="Fichas Atendidas")

@app.route('/eliminadas')
def eliminadas():
    conexion = obtener_conexion()
    fichas = conexion.execute('SELECT * FROM ficha WHERE eliminado = 1').fetchall()
    conexion.close()
    return render_template('index.html', fichas=fichas, title="Fichas Eliminadas")


@app.route('/add', methods=['POST'])
def add_ficha():
    nombre = request.form['nombre']
    edad = request.form['edad']
    area = request.form['area']
    if nombre:
        conexion = obtener_conexion()
        conexion.execute('INSERT INTO ficha (nombre, edad, area, done) VALUES (?, ?, ?, ?)',
                         (nombre, edad, area, 0))
        conexion.commit()
        conexion.close()
    return redirect(url_for('index'))
@app.route("/atendido/<int:ficha_id>")
def marcar_atendida(ficha_id):
    conexion = obtener_conexion()
    conexion.execute('UPDATE ficha SET done = 1 WHERE id = ?', (ficha_id,))
    conexion.commit()
    conexion.close()
    return redirect(request.referrer or url_for('index'))
@app.route("/eliminar/<int:ficha_id>")
def eliminar_ficha(ficha_id):
    conexion = obtener_conexion()
    conexion.execute('UPDATE ficha SET eliminado = 1 WHERE id = ?', (ficha_id,))
    conexion.commit()
    conexion.close()
    return redirect(request.referrer or url_for('index'))

@app.route('/restaurar/<int:ficha_id>')
def restaurar_ficha(ficha_id):
    conexion = obtener_conexion()
    conexion.execute('UPDATE ficha SET eliminado = 0 WHERE id = ?', (ficha_id,))
    conexion.commit()
    conexion.close()
    return redirect(url_for('eliminadas'))


@app.route('/api/fichas')
def api_fichas():
    conexion = obtener_conexion()
    fichas = conexion.execute('SELECT * FROM ficha').fetchall()
    conexion.close()
    return jsonify([ dict(ficha) for ficha in fichas])

@app.route('/api/pendientes')
def api_pendientes():
    conexion = obtener_conexion()
    fichas = conexion.execute('SELECT * FROM ficha WHERE done = 0').fetchall()
    conexion.close()
    return jsonify([ dict(ficha) for ficha in fichas])

@app.route('/api/atendidas')
def api_atendidas():
    conexion = obtener_conexion()
    fichas = conexion.execute('SELECT * FROM ficha WHERE done = 1').fetchall()
    conexion.close()
    return jsonify([ dict(ficha) for ficha in fichas])

@app.route('/filtrar')
def filtrar_por_area():
    area = request.args.get('area')  # Ej: "Pediatría"
    conexion = obtener_conexion()
    fichas = conexion.execute('SELECT * FROM ficha WHERE area = ?', (area,)).fetchall()
    conexion.close()
    return render_template('index.html', fichas=fichas, title=f"Fichas en Área: {area}")



if __name__ == '__main__':
    app.run(debug=True)