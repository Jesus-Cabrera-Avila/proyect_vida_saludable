import sqlite3

def conectar():
    conexion = sqlite3.connect("vida_saludable.db")
    conexion.row_factory = sqlite3.Row
    return conexion


def crear_tabla():
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS alumnos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT,
        peso REAL,
        estatura REAL,
        imc REAL,
        clasificacion TEXT
    )
    """)

    conexion.commit()
    conexion.close()