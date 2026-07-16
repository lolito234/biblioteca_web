from flask import render_template, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash

from app import app
from config import get_conexion


# =========================
# 👤 PERFIL
# =========================
@app.route("/perfil")
def perfil():

    if "usuario" not in session:
        return redirect("/login")

    conexion = get_conexion()
    cursor = conexion.cursor()

    cursor.execute(
        """
        SELECT
            id_usuario,
            nombre,
            correo,
            rol
        FROM usuarios
        WHERE nombre=%s
        """,
        (session["usuario"],)
    )

    usuario = cursor.fetchone()

    cursor.close()

    return render_template(
        "perfil.html",
        usuario=usuario
    )


# =========================
# ✏ EDITAR PERFIL
# =========================
@app.route("/editar_perfil", methods=["GET", "POST"])
def editar_perfil():

    if "usuario" not in session:
        return redirect("/login")

    conexion = get_conexion()
    cursor = conexion.cursor()

    if request.method == "POST":

        nombre = request.form["nombre"]
        correo = request.form["correo"]

        try:

            cursor.execute(
                """
                UPDATE usuarios
                SET
                    nombre=%s,
                    correo=%s
                WHERE nombre=%s
                """,
                (
                    nombre,
                    correo,
                    session["usuario"]
                )
            )

            conexion.commit()

            session["usuario"] = nombre

            cursor.close()

            return redirect("/perfil")

        except Exception as e:

            conexion.rollback()

            return str(e)

    cursor.execute(
        """
        SELECT
            id_usuario,
            nombre,
            correo
        FROM usuarios
        WHERE nombre=%s
        """,
        (session["usuario"],)
    )

    usuario = cursor.fetchone()

    cursor.close()

    return render_template(
        "editar_perfil.html",
        usuario=usuario
    )


# =========================
# 🔒 CAMBIAR CONTRASEÑA
# =========================
@app.route("/cambiar_password", methods=["GET", "POST"])
def cambiar_password():

    if "usuario" not in session:
        return redirect("/login")

    if request.method == "POST":

        actual = request.form["actual"]
        nueva = request.form["nueva"]

        conexion = get_conexion()
        cursor = conexion.cursor()

        cursor.execute(
            """
            SELECT contrasena
            FROM usuarios
            WHERE nombre=%s
            """,
            (session["usuario"],)
        )

        usuario = cursor.fetchone()

        if not check_password_hash(usuario[0], actual):

            cursor.close()

            return "❌ La contraseña actual es incorrecta."

        nueva_hash = generate_password_hash(nueva)

        cursor.execute(
            """
            UPDATE usuarios
            SET contrasena=%s
            WHERE nombre=%s
            """,
            (
                nueva_hash,
                session["usuario"]
            )
        )

        conexion.commit()

        cursor.close()

        return redirect("/perfil")

    return render_template("cambiar_password.html")
