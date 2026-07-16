import os
import psycopg2
from flask import g

DATABASE_URL = os.environ.get("DATABASE_URL")


def get_conexion():
    """Devuelve una conexión por request, guardada en el contexto de Flask (g)."""

    if "db" not in g:
        if DATABASE_URL:
            g.db = psycopg2.connect(DATABASE_URL)
        else:
            g.db = psycopg2.connect(
                host=os.environ.get("DB_HOST", "localhost"),
                database=os.environ.get("DB_NAME", "biblioteca_web"),
                user=os.environ.get("DB_USER", "postgres"),
                password=os.environ.get("DB_PASSWORD", "adriano123456"),
                port=os.environ.get("DB_PORT", "5432"),
            )

    return g.db


def close_conexion(e=None):
    db = g.pop("db", None)

    if db is not None:
        db.close()