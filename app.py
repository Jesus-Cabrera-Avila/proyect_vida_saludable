from flask import Flask, render_template, request
from database import conectar, crear_tabla

app = Flask(__name__)

# Página principal
@app.route('/')
def inicio():
    return render_template('index.html')


# Página IMC (guardar datos)
@app.route('/imc', methods=['GET', 'POST'])
def imc():

    if request.method == 'POST':

        # Obtener datos del formulario
        nombre = request.form['nombre']
        sexo = request.form['sexo']
        peso = float(request.form['peso'])
        estatura = float(request.form['estatura'])

        # Calcular IMC
        resultado_imc = peso / (estatura ** 2)

        # Clasificación + imágenes según sexo
        if resultado_imc < 18.5:
            clasificacion = "Bajo peso"
            recomendacion = "Consumir alimentos nutritivos y aumentar calorías saludables."

            if sexo == "hombre":
                imagen_imc = "img/bajo_peso_hombre.png"
            else:
                imagen_imc = "img/bajo_peso_mujer.png"

        elif resultado_imc <= 24.9:
            clasificacion = "Peso normal"
            recomendacion = "Mantener buena alimentación y ejercicio regular."

            if sexo == "hombre":
                imagen_imc = "img/normal_hombre.png"
            else:
                imagen_imc = "img/normal_mujer.png"

        elif resultado_imc <= 29.9:
            clasificacion = "Sobrepeso"
            recomendacion = "Reducir comida chatarra y realizar actividad física."

            if sexo == "hombre":
                imagen_imc = "img/sobrepeso_hombre.png"
            else:
                imagen_imc = "img/sobrepeso_mujer.png"

        elif resultado_imc <= 34.9:
            clasificacion = "Obesidad grado I"
            recomendacion = "Consultar nutricionista y hacer ejercicio constante."

            if sexo == "hombre":
                imagen_imc = "img/obesidad1_hombre.png"
            else:
                imagen_imc = "img/obesidad1_mujer.png"

        elif resultado_imc <= 39.9:
            clasificacion = "Obesidad grado II"
            recomendacion = "Cambiar hábitos alimenticios y supervisión médica."

            if sexo == "hombre":
                imagen_imc = "img/obesidad2_hombre.png"
            else:
                imagen_imc = "img/obesidad2_mujer.png"

        else:
            clasificacion = "Obesidad grado III"
            recomendacion = "Atención médica inmediata y plan alimenticio especializado."

            if sexo == "hombre":
                imagen_imc = "img/obesidad3_hombre.png"
            else:
                imagen_imc = "img/obesidad3_mujer.png"

        # Guardar en base de datos
        conexion = conectar()
        cursor = conexion.cursor()

        sql = """
        INSERT INTO alumnos(nombre, peso, estatura, imc, clasificacion)
        VALUES (?, ?, ?, ?, ?)
        """

        valores = (
            nombre,
            peso,
            estatura,
            resultado_imc,
            clasificacion
        )

        cursor.execute(sql, valores)
        conexion.commit()

        cursor.close()
        conexion.close()

        # Mostrar resultado
        return render_template(
            'resultado.html',
            nombre=nombre,
            imc=round(resultado_imc, 2),
            clasificacion=clasificacion,
            recomendacion=recomendacion,
            imagen_imc=imagen_imc
        )

    return render_template('imc.html')


# Mostrar alumnos (historial)
@app.route('/alumnos')
def alumnos():

    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM alumnos")
    datos = [dict(fila) for fila in cursor.fetchall()]

    cursor.close()
    conexion.close()

    return render_template("alumnos.html", alumnos=datos)


# Ejecutar servidor
if __name__ == '__main__':
    crear_tabla()
    app.run(debug=True)