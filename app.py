from flask import Flask, render_template, request, redirect, session
import psycopg2
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# 🔐 Seguridad de sesión
app.secret_key = 'clave_super_segura_123456'
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

# 🔗 Conexión a PostgreSQL
conexion = psycopg2.connect(
    host="localhost",
    database="biblioteca_web",
    user="admin",
    password="admin123"
)

# =========================
# 🏠 INICIO
# =========================
@app.route('/')
def inicio():
    usuario = session.get('usuario')

    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM libros")
    libros = cursor.fetchall()
    cursor.close()

    return render_template("index.html", usuario=usuario, libros=libros)


# =========================
# 📝 REGISTRO (SEGURO)
# =========================
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form['nombre']
        correo = request.form['correo']
        contrasena = request.form['contrasena']

        try:
            cursor = conexion.cursor()

            # 🔐 Hash de contraseña
            hash_contrasena = generate_password_hash(contrasena)

            cursor.execute(
                "INSERT INTO usuarios (nombre, correo, contrasena) VALUES (%s, %s, %s)",
                (nombre, correo, hash_contrasena)
            )

            conexion.commit()
            cursor.close()

            return redirect('/login')

        except Exception as e:
            conexion.rollback()
            return f"Error en registro: {e}"

    return render_template("registro.html")


# =========================
# 🔐 LOGIN (SEGURO)
# =========================
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo = request.form['correo']
        contrasena = request.form['contrasena']

        try:
            cursor = conexion.cursor()

            cursor.execute(
                "SELECT * FROM usuarios WHERE correo=%s",
                (correo,)
            )

            usuario = cursor.fetchone()
            cursor.close()

            if usuario and check_password_hash(usuario[3], contrasena):
                session['usuario'] = usuario[1]
                return redirect('/')
            else:
                return "❌ Correo o contraseña incorrectos"

        except Exception as e:
            return f"Error en login: {e}"

    return render_template("login.html")


# =========================
# 🚪 LOGOUT
# =========================
@app.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect('/')


# =========================
# 📚 AGREGAR LIBRO (SIN DUPLICADOS)
# =========================
@app.route('/agregar_libro', methods=['GET', 'POST'])
def agregar_libro():
    mensaje = None

    if request.method == 'POST':
        titulo = request.form['titulo']
        autor = request.form['autor']
        categoria = request.form['categoria']
        stock = request.form['stock']
        descripcion = request.form['descripcion']

        try:
            cursor = conexion.cursor()

            cursor.execute(
                "SELECT * FROM libros WHERE titulo=%s AND autor=%s",
                (titulo, autor)
            )
            existe = cursor.fetchone()

            if existe:
                mensaje = "⚠️ Este libro ya existe"
            else:
                cursor.execute(
                    "INSERT INTO libros (titulo, autor, categoria, stock, descripcion) VALUES (%s, %s, %s, %s, %s)",
                    (titulo, autor, categoria, stock, descripcion)
                )
                conexion.commit()
                mensaje = "✅ Libro agregado"

            cursor.close()

        except Exception as e:
            conexion.rollback()
            mensaje = f"Error: {e}"

    return render_template("agregar_libro.html", mensaje=mensaje)


# =========================
# 📖 RESERVAR (SEGURO)
# =========================
@app.route('/reservar/<int:id_libro>', methods=['POST'])
def reservar(id_libro):
    if 'usuario' not in session:
        return redirect('/login')

    try:
        cursor = conexion.cursor()

        # Usuario
        cursor.execute(
            "SELECT id_usuario FROM usuarios WHERE nombre=%s",
            (session['usuario'],)
        )
        usuario = cursor.fetchone()

        if not usuario:
            return "Usuario no encontrado"

        id_usuario = usuario[0]

        # 🔒 Verificar stock
        cursor.execute(
            "SELECT stock FROM libros WHERE id_libro=%s",
            (id_libro,)
        )
        stock = cursor.fetchone()

        if not stock or stock[0] <= 0:
            return "❌ No hay stock disponible"

        # Insertar reserva
        cursor.execute(
            "INSERT INTO reservas (id_usuario, id_libro, fecha_reserva, estado) VALUES (%s, %s, CURRENT_DATE, 'reservado')",
            (id_usuario, id_libro)
        )

        # Reducir stock
        cursor.execute(
            "UPDATE libros SET stock = stock - 1 WHERE id_libro=%s",
            (id_libro,)
        )

        conexion.commit()
        cursor.close()

        return redirect('/')

    except Exception as e:
        conexion.rollback()
        return f"Error: {e}"


# =========================
# 📌 MIS RESERVAS
# =========================
@app.route('/mis_reservas')
def mis_reservas():
    if 'usuario' not in session:
        return redirect('/login')

    cursor = conexion.cursor()

    cursor.execute(
        "SELECT id_usuario FROM usuarios WHERE nombre=%s",
        (session['usuario'],)
    )
    usuario = cursor.fetchone()
    id_usuario = usuario[0]

    cursor.execute("""
        SELECT reservas.id_reserva, libros.titulo, libros.autor, reservas.id_libro
        FROM reservas
        JOIN libros ON reservas.id_libro = libros.id_libro
        WHERE reservas.id_usuario = %s
    """, (id_usuario,))

    reservas = cursor.fetchall()
    cursor.close()

    return render_template("mis_reservas.html", reservas=reservas)


# =========================
# ❌ CANCELAR RESERVA
# =========================
@app.route('/cancelar_reserva/<int:id_reserva>/<int:id_libro>', methods=['POST'])
def cancelar_reserva(id_reserva, id_libro):
    if 'usuario' not in session:
        return redirect('/login')

    try:
        cursor = conexion.cursor()

        cursor.execute(
            "DELETE FROM reservas WHERE id_reserva=%s",
            (id_reserva,)
        )

        cursor.execute(
            "UPDATE libros SET stock = stock + 1 WHERE id_libro=%s",
            (id_libro,)
        )

        conexion.commit()
        cursor.close()

        return redirect('/mis_reservas')

    except Exception as e:
        conexion.rollback()
        return f"Error: {e}"


# =========================
# 📊 TODAS LAS RESERVAS (ADMIN SIMPLE)
# =========================
@app.route('/todas_reservas')
def todas_reservas():
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT usuarios.nombre, libros.titulo, reservas.fecha_reserva, reservas.estado
        FROM reservas
        JOIN usuarios ON reservas.id_usuario = usuarios.id_usuario
        JOIN libros ON reservas.id_libro = libros.id_libro
    """)

    reservas = cursor.fetchall()
    cursor.close()

    return render_template("todas_reservas.html", reservas=reservas)


# =========================
# 🚀 RUN
# =========================
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)