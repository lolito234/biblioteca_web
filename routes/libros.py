from flask import render_template, request, redirect, session
from werkzeug.utils import secure_filename
import os

from app import app
from config import get_conexion

UPLOAD_FOLDER = os.path.join("static", "img", "libros")


# =========================
# 🏠 INICIO
# =========================
@app.route("/")
def inicio():

    usuario = session.get("usuario")
    rol = session.get("rol")
    q = request.args.get("q", "").strip()

    conexion = get_conexion()

    try:

        cursor = conexion.cursor()

        if q:
            cursor.execute(
                """
                SELECT *
                FROM libros
                WHERE titulo ILIKE %s OR autor ILIKE %s
                ORDER BY id_libro
                """,
                (f"%{q}%", f"%{q}%")
            )
        else:
            cursor.execute("""
                SELECT *
                FROM libros
                ORDER BY id_libro
            """)

        libros = cursor.fetchall()

        cursor.close()

    except Exception as e:

        conexion.rollback()
        print(e)

        libros = []

    return render_template(
        "index.html",
        usuario=usuario,
        rol=rol,
        libros=libros,
        q=q
    )


# =========================
# ➕ AGREGAR LIBRO
# =========================
@app.route("/agregar_libro", methods=["GET", "POST"])
def agregar_libro():

    if "usuario" not in session:
        return redirect("/login")

    if session.get("rol") != "admin":
        return "⛔ Acceso denegado.", 403

    mensaje = None

    if request.method == "POST":

        titulo = request.form["titulo"]
        autor = request.form["autor"]
        categoria = request.form["categoria"]
        stock = request.form["stock"]
        descripcion = request.form["descripcion"]

        imagen = request.files.get("imagen")

        nombre_imagen = None

        if imagen and imagen.filename:

            nombre_imagen = secure_filename(imagen.filename)

            os.makedirs(UPLOAD_FOLDER, exist_ok=True)

            imagen.save(
                os.path.join(
                    UPLOAD_FOLDER,
                    nombre_imagen
                )
            )

        try:

            conexion = get_conexion()
            cursor = conexion.cursor()

            cursor.execute("""
                INSERT INTO libros
                (
                    titulo,
                    autor,
                    categoria,
                    stock,
                    descripcion,
                    imagen
                )
                VALUES
                (%s,%s,%s,%s,%s,%s)
            """,
            (
                titulo,
                autor,
                categoria,
                stock,
                descripcion,
                nombre_imagen
            ))

            conexion.commit()

            cursor.close()

            mensaje = "✅ Libro agregado correctamente"

        except Exception as e:

            conexion.rollback()

            mensaje = str(e)

    return render_template(
        "agregar_libro.html",
        mensaje=mensaje
    )


# =========================
# 📚 ADMINISTRAR LIBROS
# =========================
@app.route("/libros_admin")
def libros_admin():

    if "usuario" not in session:
        return redirect("/login")

    if session.get("rol") != "admin":
        return "Acceso denegado", 403

    conexion = get_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT *
        FROM libros
        ORDER BY id_libro
    """)

    libros = cursor.fetchall()

    cursor.close()

    return render_template(
        "libros_admin.html",
        libros=libros
    )


# =========================
# 🗑 ELIMINAR LIBRO
# =========================
@app.route("/eliminar_libro/<int:id_libro>")
def eliminar_libro(id_libro):

    if "usuario" not in session:
        return redirect("/login")

    if session.get("rol") != "admin":
        return "Acceso denegado"

    conexion = get_conexion()

    try:

        cursor = conexion.cursor()

        cursor.execute(
            "DELETE FROM libros WHERE id_libro=%s",
            (id_libro,)
        )

        conexion.commit()

        cursor.close()

        return redirect("/libros_admin")

    except Exception as e:

        conexion.rollback()

        return str(e)


# =========================
# ✏ EDITAR LIBRO
# =========================
@app.route("/editar_libro/<int:id_libro>", methods=["GET", "POST"])
def editar_libro(id_libro):

    if "usuario" not in session:
        return redirect("/login")

    if session.get("rol") != "admin":
        return "Acceso denegado"

    conexion = get_conexion()
    cursor = conexion.cursor()

    if request.method == "POST":

        titulo = request.form["titulo"]
        autor = request.form["autor"]
        categoria = request.form["categoria"]
        stock = request.form["stock"]
        descripcion = request.form["descripcion"]

        imagen = request.files.get("imagen")

        if imagen and imagen.filename:

            nombre_imagen = secure_filename(imagen.filename)

            os.makedirs(UPLOAD_FOLDER, exist_ok=True)

            imagen.save(
                os.path.join(
                    UPLOAD_FOLDER,
                    nombre_imagen
                )
            )

            cursor.execute("""
                UPDATE libros
                SET
                    titulo=%s,
                    autor=%s,
                    categoria=%s,
                    stock=%s,
                    descripcion=%s,
                    imagen=%s
                WHERE id_libro=%s
            """,
            (
                titulo,
                autor,
                categoria,
                stock,
                descripcion,
                nombre_imagen,
                id_libro
            ))

        else:

            cursor.execute("""
                UPDATE libros
                SET
                    titulo=%s,
                    autor=%s,
                    categoria=%s,
                    stock=%s,
                    descripcion=%s
                WHERE id_libro=%s
            """,
            (
                titulo,
                autor,
                categoria,
                stock,
                descripcion,
                id_libro
            ))

        conexion.commit()

        cursor.close()

        return redirect("/libros_admin")

    cursor.execute(
        "SELECT * FROM libros WHERE id_libro=%s",
        (id_libro,)
    )

    libro = cursor.fetchone()

    cursor.close()

    return render_template(
        "editar_libro.html",
        libro=libro
    )