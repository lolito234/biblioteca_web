from flask import render_template, redirect, session
from app import app
from config import get_conexion

DIAS_PRESTAMO = 14


# =========================
# 📖 RESERVAR LIBRO
# =========================
@app.route('/reservar/<int:id_libro>', methods=['POST'])
def reservar(id_libro):

    if 'usuario' not in session:
        return redirect('/login')

    conexion = get_conexion()

    try:

        cursor = conexion.cursor()

        cursor.execute(
            "SELECT id_usuario FROM usuarios WHERE nombre=%s",
            (session['usuario'],)
        )

        usuario = cursor.fetchone()

        if not usuario:
            return "Usuario no encontrado"

        id_usuario = usuario[0]

        cursor.execute(
            "SELECT stock FROM libros WHERE id_libro=%s",
            (id_libro,)
        )

        stock = cursor.fetchone()

        if not stock:
            return "❌ Libro no encontrado"

        if stock[0] <= 0:
            return "❌ No hay stock disponible"

        cursor.execute(
            """
            SELECT id_reserva FROM reservas
            WHERE id_usuario=%s AND id_libro=%s AND estado='reservado'
            """,
            (id_usuario, id_libro)
        )

        if cursor.fetchone():
            return "❌ Ya tienes una reserva activa de este libro"

        cursor.execute("""
            INSERT INTO reservas
            (
                id_usuario,
                id_libro,
                fecha_reserva,
                fecha_limite,
                estado
            )
            VALUES
            (%s,%s,CURRENT_DATE,CURRENT_DATE + make_interval(days => %s),'reservado')
        """,
        (
            id_usuario,
            id_libro,
            DIAS_PRESTAMO
        ))

        cursor.execute(
            "UPDATE libros SET stock=stock-1 WHERE id_libro=%s",
            (id_libro,)
        )

        conexion.commit()

        cursor.close()

        return redirect('/')

    except Exception as e:

        conexion.rollback()

        return str(e)


# =========================
# 📚 MIS RESERVAS
# =========================
@app.route('/mis_reservas')
def mis_reservas():

    if 'usuario' not in session:
        return redirect('/login')

    conexion = get_conexion()
    cursor = conexion.cursor()

    cursor.execute(
        "SELECT id_usuario FROM usuarios WHERE nombre=%s",
        (session['usuario'],)
    )

    usuario = cursor.fetchone()

    id_usuario = usuario[0]

    cursor.execute("""

        SELECT

        reservas.id_reserva,

        libros.titulo,

        libros.autor,

        reservas.id_libro,

        reservas.fecha_reserva,

        reservas.estado,

        reservas.fecha_limite

        FROM reservas

        INNER JOIN libros

        ON reservas.id_libro=libros.id_libro

        WHERE reservas.id_usuario=%s

        ORDER BY reservas.fecha_reserva DESC

    """, (id_usuario,))

    reservas = cursor.fetchall()

    cursor.close()

    return render_template(

        "mis_reservas.html",

        reservas=reservas

    )


# =========================
# ❌ CANCELAR RESERVA
# =========================
@app.route('/cancelar_reserva/<int:id_reserva>/<int:id_libro>', methods=['POST'])
def cancelar_reserva(id_reserva, id_libro):

    if 'usuario' not in session:
        return redirect('/login')

    conexion = get_conexion()

    try:

        cursor = conexion.cursor()

        cursor.execute(
            """
            DELETE FROM reservas
            WHERE id_reserva=%s
              AND id_libro=%s
              AND estado='reservado'
              AND id_usuario=(SELECT id_usuario FROM usuarios WHERE nombre=%s)
            """,
            (id_reserva, id_libro, session['usuario'])
        )

        if cursor.rowcount == 0:
            conexion.rollback()
            cursor.close()
            return "❌ Reserva no encontrada", 404

        cursor.execute(
            "UPDATE libros SET stock=stock+1 WHERE id_libro=%s",
            (id_libro,)
        )

        conexion.commit()

        cursor.close()

        return redirect('/mis_reservas')

    except Exception as e:

        conexion.rollback()

        return str(e)


# =========================
# 📦 SOLICITAR DEVOLUCIÓN
# =========================
@app.route('/solicitar_devolucion/<int:id_reserva>', methods=['POST'])
def solicitar_devolucion(id_reserva):

    if 'usuario' not in session:
        return redirect('/login')

    conexion = get_conexion()

    try:

        cursor = conexion.cursor()

        cursor.execute(
            """
            SELECT reservas.id_usuario, reservas.id_libro
            FROM reservas
            WHERE reservas.id_reserva=%s
              AND reservas.estado='reservado'
              AND reservas.id_usuario=(SELECT id_usuario FROM usuarios WHERE nombre=%s)
            """,
            (id_reserva, session['usuario'])
        )

        reserva = cursor.fetchone()

        if not reserva:
            conexion.rollback()
            cursor.close()
            return "❌ Reserva no encontrada", 404

        id_usuario, id_libro = reserva

        cursor.execute(
            """
            INSERT INTO devoluciones (id_reserva, id_usuario, id_libro)
            VALUES (%s, %s, %s)
            """,
            (id_reserva, id_usuario, id_libro)
        )

        cursor.execute(
            "UPDATE reservas SET estado='en_revision' WHERE id_reserva=%s",
            (id_reserva,)
        )

        conexion.commit()

        cursor.close()

        return redirect('/mis_reservas')

    except Exception as e:

        conexion.rollback()

        return str(e)
