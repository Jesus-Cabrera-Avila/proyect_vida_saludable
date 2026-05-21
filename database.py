import sqlite3

# CONEXIÓN A SQLITE
def conectar():

    conexion = sqlite3.connect("vida_saludable.db")

    # Permite acceder por nombre de columna
    conexion.row_factory = sqlite3.Row

    return conexion

# CREAR TABLAS
def crear_tablas():

    conexion = conectar()
    cursor = conexion.cursor()

    # TABLA ALUMNOS (IMC)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS alumnos (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        nombre TEXT NOT NULL,

        sexo TEXT NOT NULL,

        peso REAL NOT NULL,

        estatura REAL NOT NULL,

        imc REAL NOT NULL,

        clasificacion TEXT NOT NULL

    )
    """)

    # TABLA RECETAS
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS recetas (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        nombre TEXT NOT NULL,

        descripcion TEXT NOT NULL,

        ingredientes TEXT NOT NULL,

        preparacion TEXT NOT NULL,

        tips TEXT,

        imagen TEXT

    )
    """)

    conexion.commit()

    cursor.close()
    conexion.close()


# EJECUTAR AUTOMÁTICAMENTE
crear_tablas()