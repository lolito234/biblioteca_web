from flask import Flask
import os

from config import close_conexion

app = Flask(__name__)

app.secret_key = os.environ.get("SECRET_KEY", "clave_super_segura")
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

app.teardown_appcontext(close_conexion)

# Importar todas las rutas
import routes.auth
import routes.libros
import routes.reservas
import routes.admin
import routes.usuarios