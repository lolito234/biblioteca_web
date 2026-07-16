from flask import render_template, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash

from app import app
from config import get_conexion


# =========================
# 📝 REGISTRO
# =========================
@app.route('/registro', methods=['GET', 'POST'])
def registro():

    if request.method == 'POST':

        nombre = request.form['nombre']
        correo = request.form['correo']
        contrasena = request.form['contrasena']

        try:

            conexion = get_conexion()
            cursor = conexion.cursor()

            hash_pass = generate_password_hash(contrasena)

            cursor.execute("""
                INSERT INTO usuarios
                (nombre, correo, contrasena)
                VALUES (%s,%s,%s)
            """, (nombre, correo, hash_pass))

            conexion.commit()
            cursor.close()

            return redirect('/login')

        except Exception as e:

            conexion.rollback()
            return f"Error: {e}"

    return render_template("registro.html")


# =========================
# 🔐 LOGIN
# =========================
@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        correo = request.form['correo']
        contrasena = request.form['contrasena']

        try:

            conexion = get_conexion()
            cursor = conexion.cursor()

            cursor.execute("""
                SELECT
                    id_usuario,
                    nombre,
                    correo,
                    contrasena,
                    rol
                FROM usuarios
                WHERE correo=%s
            """, (correo,))

            usuario = cursor.fetchone()

            cursor.close()

            if usuario and check_password_hash(usuario[3], contrasena):

                session['usuario'] = usuario[1]
                session['rol'] = usuario[4]

                return redirect('/')

            return "❌ Credenciales incorrectas"

        except Exception as e:

            conexion.rollback()
            return f"Error: {e}"

    return render_template("login.html")


# =========================
# 🚪 LOGOUT
# =========================
@app.route('/logout')
def logout():

    session.clear()

    return redirect('/')