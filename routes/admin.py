from flask import render_template, request, redirect, session

from app import app
from config import get_conexion


# =========================
# 👑 PANEL ADMIN
# =========================
@app.route('/admin')
def admin():

    if 'usuario' not in session:
        return redirect('/login')

    if session.get('rol') != 'admin':
        return "⛔ Acceso denegado", 403

    conexion = get_conexion()

    try:

        cursor = conexion.cursor()

        cursor.execute("SELECT COUNT(*) FROM libros")
        total_libros = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM usuarios")
        total_usuarios = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM reservas")
        total_reservas = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM devoluciones WHERE estado_libro IS NULL")
        total_devoluciones_pendientes = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM sanciones WHERE estado='pendiente'")
        total_sanciones_pendientes = cursor.fetchone()[0]

        cursor.close()

        return render_template(
            "admin.html",
            total_libros=total_libros,
            total_usuarios=total_usuarios,
            total_reservas=total_reservas,
            total_devoluciones_pendientes=total_devoluciones_pendientes,
            total_sanciones_pendientes=total_sanciones_pendientes
        )

    except Exception as e:

        conexion.rollback()
        return str(e)


# =========================
# 👥 ADMINISTRAR USUARIOS
# =========================
@app.route('/usuarios')
def usuarios():

    if 'usuario' not in session:
        return redirect('/login')

    if session.get('rol') != 'admin':
        return "Acceso denegado", 403

    conexion = get_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT
            id_usuario,
            nombre,
            correo,
            rol
        FROM usuarios
        ORDER BY id_usuario
    """)

    usuarios = cursor.fetchall()

    cursor.close()

    return render_template(
        "usuarios.html",
        usuarios=usuarios
    )


# =========================
# ✏ EDITAR USUARIO
# =========================
@app.route('/editar_usuario/<int:id>', methods=['GET', 'POST'])
def editar_usuario(id):

    if 'usuario' not in session:
        return redirect('/login')

    if session.get('rol') != 'admin':
        return "Acceso denegado", 403

    conexion = get_conexion()
    cursor = conexion.cursor()

    if request.method == 'POST':

        nombre = request.form['nombre']
        correo = request.form['correo']
        rol = request.form['rol']

        try:

            cursor.execute("""
                UPDATE usuarios
                SET
                    nombre=%s,
                    correo=%s,
                    rol=%s
                WHERE id_usuario=%s
            """, (nombre, correo, rol, id))

            conexion.commit()

            cursor.close()

            return redirect('/usuarios')

        except Exception as e:

            conexion.rollback()

            return str(e)

    cursor.execute(
        "SELECT id_usuario,nombre,correo,rol FROM usuarios WHERE id_usuario=%s",
        (id,)
    )

    usuario = cursor.fetchone()

    cursor.close()

    return render_template(
        "editar_usuario.html",
        usuario=usuario
    )


# =========================
# 🗑 ELIMINAR USUARIO
# =========================
@app.route('/eliminar_usuario/<int:id>')
def eliminar_usuario(id):

    if 'usuario' not in session:
        return redirect('/login')

    if session.get('rol') != 'admin':
        return "Acceso denegado"

    conexion = get_conexion()

    try:

        cursor = conexion.cursor()

        cursor.execute(
            "DELETE FROM usuarios WHERE id_usuario=%s",
            (id,)
        )

        conexion.commit()

        cursor.close()

        return redirect('/usuarios')

    except Exception as e:

        conexion.rollback()

        return str(e)


# =========================
# 📚 TODAS LAS RESERVAS
# =========================
@app.route('/reservas_admin')
def reservas_admin():

    if 'usuario' not in session:
        return redirect('/login')

    if session.get('rol') != 'admin':
        return "Acceso denegado", 403

    conexion = get_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT
            reservas.id_reserva,
            usuarios.nombre,
            libros.titulo,
            reservas.fecha_reserva,
            reservas.estado
        FROM reservas
        INNER JOIN usuarios
            ON reservas.id_usuario=usuarios.id_usuario
        INNER JOIN libros
            ON reservas.id_libro=libros.id_libro
        ORDER BY reservas.id_reserva DESC
    """)

    reservas = cursor.fetchall()

    cursor.close()

    return render_template(
        "reservas_admin.html",
        reservas=reservas
    )


# =========================
# ❌ ELIMINAR RESERVA
# =========================
@app.route('/eliminar_reserva/<int:id>')
def eliminar_reserva(id):

    if 'usuario' not in session:
        return redirect('/login')

    if session.get('rol') != 'admin':
        return "Acceso denegado"

    conexion = get_conexion()

    try:

        cursor = conexion.cursor()

        cursor.execute(
            "SELECT id_libro FROM reservas WHERE id_reserva=%s",
            (id,)
        )

        reserva = cursor.fetchone()

        cursor.execute(
            "DELETE FROM reservas WHERE id_reserva=%s",
            (id,)
        )

        if reserva:
            cursor.execute(
                "UPDATE libros SET stock=stock+1 WHERE id_libro=%s",
                (reserva[0],)
            )

        conexion.commit()

        cursor.close()

        return redirect('/reservas_admin')

    except Exception as e:

        conexion.rollback()

        return str(e)


# =========================
# 📦 DEVOLUCIONES PENDIENTES
# =========================
@app.route('/devoluciones_admin')
def devoluciones_admin():

    if 'usuario' not in session:
        return redirect('/login')

    if session.get('rol') != 'admin':
        return "Acceso denegado", 403

    conexion = get_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT
            devoluciones.id_devolucion,
            usuarios.nombre,
            libros.titulo,
            devoluciones.id_libro,
            devoluciones.fecha_solicitud
        FROM devoluciones
        INNER JOIN usuarios ON devoluciones.id_usuario=usuarios.id_usuario
        INNER JOIN libros ON devoluciones.id_libro=libros.id_libro
        WHERE devoluciones.estado_libro IS NULL
        ORDER BY devoluciones.fecha_solicitud
    """)

    devoluciones = cursor.fetchall()

    cursor.close()

    return render_template(
        "devoluciones_admin.html",
        devoluciones=devoluciones
    )


# =========================
# ✅ VERIFICAR DEVOLUCIÓN
# =========================
@app.route('/verificar_devolucion/<int:id_devolucion>', methods=['POST'])
def verificar_devolucion(id_devolucion):

    if 'usuario' not in session:
        return redirect('/login')

    if session.get('rol') != 'admin':
        return "Acceso denegado", 403

    estado_libro = request.form['estado_libro']
    observaciones = request.form.get('observaciones', '')
    multa = request.form.get('multa') or 0

    if estado_libro not in ('bueno', 'dañado'):
        return "Estado inválido", 400

    conexion = get_conexion()

    try:

        cursor = conexion.cursor()

        cursor.execute(
            """
            SELECT id_reserva, id_usuario, id_libro
            FROM devoluciones
            WHERE id_devolucion=%s AND estado_libro IS NULL
            """,
            (id_devolucion,)
        )

        devolucion = cursor.fetchone()

        if not devolucion:
            conexion.rollback()
            cursor.close()
            return "❌ Devolución no encontrada o ya verificada", 404

        id_reserva, id_usuario, id_libro = devolucion

        cursor.execute(
            """
            UPDATE devoluciones
            SET estado_libro=%s, observaciones=%s, fecha_verificacion=CURRENT_DATE
            WHERE id_devolucion=%s
            """,
            (estado_libro, observaciones, id_devolucion)
        )

        cursor.execute(
            "UPDATE reservas SET estado='devuelto' WHERE id_reserva=%s",
            (id_reserva,)
        )

        cursor.execute(
            "UPDATE libros SET stock=stock+1, estado=%s WHERE id_libro=%s",
            (estado_libro, id_libro)
        )

        if estado_libro == 'dañado':
            cursor.execute(
                """
                INSERT INTO sanciones (id_usuario, id_devolucion, motivo, multa)
                VALUES (%s, %s, %s, %s)
                """,
                (id_usuario, id_devolucion, 'Libro devuelto con daños', multa)
            )

        conexion.commit()

        cursor.close()

        return redirect('/devoluciones_admin')

    except Exception as e:

        conexion.rollback()

        return str(e)


# =========================
# ⚠ SANCIONES
# =========================
@app.route('/sanciones_admin')
def sanciones_admin():

    if 'usuario' not in session:
        return redirect('/login')

    if session.get('rol') != 'admin':
        return "Acceso denegado", 403

    conexion = get_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT
            sanciones.id_sancion,
            usuarios.nombre,
            sanciones.motivo,
            sanciones.fecha_emision,
            sanciones.multa,
            sanciones.estado
        FROM sanciones
        INNER JOIN usuarios ON sanciones.id_usuario=usuarios.id_usuario
        ORDER BY sanciones.fecha_emision DESC
    """)

    sanciones = cursor.fetchall()

    cursor.close()

    return render_template(
        "sanciones_admin.html",
        sanciones=sanciones
    )


# =========================
# 💰 MARCAR SANCIÓN COMO PAGADA
# =========================
@app.route('/marcar_sancion_pagada/<int:id_sancion>', methods=['POST'])
def marcar_sancion_pagada(id_sancion):

    if 'usuario' not in session:
        return redirect('/login')

    if session.get('rol') != 'admin':
        return "Acceso denegado", 403

    conexion = get_conexion()

    try:

        cursor = conexion.cursor()

        cursor.execute(
            "UPDATE sanciones SET estado='pagada' WHERE id_sancion=%s",
            (id_sancion,)
        )

        conexion.commit()

        cursor.close()

        return redirect('/sanciones_admin')

    except Exception as e:

        conexion.rollback()

        return str(e)
