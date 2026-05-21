from flask import Flask, render_template, request, redirect
from database import conectar, crear_tablas

app = Flask(__name__)

# Crear tablas automáticamente
crear_tablas()

# Pagina principal
@app.route('/')
def inicio():
    return render_template('index.html')

# Calculadora de IMC
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

        # Clasificación
        if resultado_imc < 18.5:

            clasificacion = "Bajo peso"

            recomendacion = (
                "Consumir alimentos nutritivos "
                "y aumentar calorías saludables."
            )

            if sexo == "hombre":
                imagen_imc = "img/bajo_peso_hombre.png"
            else:
                imagen_imc = "img/bajo_peso_mujer.png"

        elif resultado_imc <= 24.9:

            clasificacion = "Peso normal"

            recomendacion = (
                "Mantener buena alimentación "
                "y ejercicio regular."
            )

            if sexo == "hombre":
                imagen_imc = "img/normal_hombre.png"
            else:
                imagen_imc = "img/normal_mujer.png"

        elif resultado_imc <= 29.9:

            clasificacion = "Sobrepeso"

            recomendacion = (
                "Reducir comida chatarra "
                "y realizar actividad física."
            )

            if sexo == "hombre":
                imagen_imc = "img/sobrepeso_hombre.png"
            else:
                imagen_imc = "img/sobrepeso_mujer.png"

        elif resultado_imc <= 34.9:

            clasificacion = "Obesidad grado I"

            recomendacion = (
                "Consultar nutricionista "
                "y hacer ejercicio constante."
            )

            if sexo == "hombre":
                imagen_imc = "img/obesidad1_hombre.png"
            else:
                imagen_imc = "img/obesidad1_mujer.png"

        elif resultado_imc <= 39.9:

            clasificacion = "Obesidad grado II"

            recomendacion = (
                "Cambiar hábitos alimenticios "
                "y supervisión médica."
            )

            if sexo == "hombre":
                imagen_imc = "img/obesidad2_hombre.png"
            else:
                imagen_imc = "img/obesidad2_mujer.png"

        else:

            clasificacion = "Obesidad grado III"

            recomendacion = (
                "Atención médica inmediata "
                "y plan alimenticio especializado."
            )

            if sexo == "hombre":
                imagen_imc = "img/obesidad3_hombre.png"
            else:
                imagen_imc = "img/obesidad3_mujer.png"

        # Guardar en base de datos
        conexion = conectar()
        cursor = conexion.cursor()

        sql = """
        INSERT INTO alumnos
        (nombre, sexo, peso, estatura, imc, clasificacion)
        VALUES (?, ?, ?, ?, ?, ?)
        """

        valores = (
            nombre,
            sexo,
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

# Historial de alimnos
@app.route('/alumnos')
def alumnos():

    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM alumnos")

    datos = [dict(fila) for fila in cursor.fetchall()]

    cursor.close()
    conexion.close()

    return render_template(
        "alumnos.html",
        alumnos=datos
    )

# Quimica
@app.route('/quimica')
def quimica():
    return render_template('quimica.html')

# Historia
@app.route('/historia')
def historia():
    return render_template('historia.html')


# Recetas
@app.route('/recetas')
def recetas():

    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM recetas")

    datos = [dict(fila) for fila in cursor.fetchall()]

    cursor.close()
    conexion.close()

    return render_template(
        'recetas.html',
        recetas=datos
    )

# Agregar recetas
@app.route('/agregar_receta', methods=['GET', 'POST'])
def agregar_receta():

    if request.method == 'POST':

        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        ingredientes = request.form['ingredientes']
        preparacion = request.form['preparacion']
        tips = request.form['tips']
        imagen = request.form['imagen']

        conexion = conectar()
        cursor = conexion.cursor()

        sql = """
        INSERT INTO recetas
        (nombre, descripcion, ingredientes,
        preparacion, tips, imagen)
        VALUES (?, ?, ?, ?, ?, ?)
        """

        valores = (
            nombre,
            descripcion,
            ingredientes,
            preparacion,
            tips,
            imagen
        )

        cursor.execute(sql, valores)

        conexion.commit()

        cursor.close()
        conexion.close()

        return redirect('/recetas')

    return render_template('agregar_receta.html')

# Ejercicios
@app.route('/ejercicios')
def ejercicios():
    return render_template('ejercicios.html')

# Salud mental
@app.route('/salud_mental')
def salud_mental():
    return render_template('salud_mental.html')

# Ejecutar
if __name__ == '__main__':
    app.run(debug=True)