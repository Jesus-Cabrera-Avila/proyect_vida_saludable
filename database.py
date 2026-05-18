import mysql.connector

conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="vida_saludable"
)

print("Conectado correctamente")