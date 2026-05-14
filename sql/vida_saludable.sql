CREATE DATABASE vida_saludable;

USE vida_saludable;

CREATE TABLE alumnos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    peso FLOAT,
    estatura FLOAT,
    imc FLOAT,
    clasificacion VARCHAR(100)
);