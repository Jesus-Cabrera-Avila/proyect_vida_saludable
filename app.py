from flask import Flask, render_template, request
from database import conectar

app = Flask(__name__)

# -------------------------
# Página principal
# -------------------------
@app.route('/')
def inicio():
    return render_template('index.html')


# -------------------------
# Página IMC (guardar datos)
# -------------------------
@app.route('/imc', methods=['GET', 'POST'])
def imc():

    if request.method == 'POST':

        nombre = request.form['nombre']
        peso = float(request.form['peso'])
        estatura = float(request.form['estatura'])

        resultado_imc = peso / (estatura ** 2)

        # Clasificación
        if resultado_imc < 18.5:
            clasificacion = "Bajo peso"
            recomendacion = "Consumir alimentos nutritivos y aumentar calorías saludables."

        elif resultado_imc <= 24.9:
            clasificacion = "Peso normal"
            recomendacion = "Mantener buena alimentación y ejercicio regular."

        elif resultado_imc <= 29.9:
            clasificacion = "Sobrepeso"
            recomendacion = "Reducir comida chatarra y realizar actividad física."

        elif resultado_imc <= 34.9:
            clasificacion = "Obesidad grado I"
            recomendacion = "Consultar nutricionista y hacer ejercicio constante."

        elif resultado_imc <= 39.9:
            clasificacion = "Obesidad grado II"
            recomendacion = "Cambiar hábitos alimenticios y supervisión médica."

        else:
            clasificacion = "Obesidad grado III"
            recomendacion = "Atención médica inmediata y plan alimenticio especializado."

        # Guardar en base de datos
        conexion = conectar()
        cursor = conexion.cursor()

        sql = """
        INSERT INTO alumnos(nombre, peso, estatura, imc, clasificacion)
        VALUES (%s, %s, %s, %s, %s)
        """

        valores = (nombre, peso, estatura, resultado_imc, clasificacion)

        cursor.execute(sql, valores)
        conexion.commit()

        cursor.close()
        conexion.close()

        return render_template(
            'resultado.html',
            nombre=nombre,
            imc=round(resultado_imc, 2),
            clasificacion=clasificacion,
            recomendacion=recomendacion
        )

    return render_template('imc.html')


# -------------------------
# Mostrar alumnos (historial)
# -------------------------
@app.route('/alumnos')
def alumnos():

    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("SELECT * FROM alumnos")
    datos = cursor.fetchall()

    cursor.close()
    conexion.close()

    return render_template("alumnos.html", alumnos=datos)


# -------------------------
# Ejecutar servidor
# -------------------------
if __name__ == '__main__':
    app.run(debug=True)