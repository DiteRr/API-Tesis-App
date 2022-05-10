CREATE DATABASE stravadb;

USE stravadb;

CREATE TABLE Usuario(
    ID INT NOT NULL PRIMARY KEY,
    username VARCHAR(50),
    firstname VARCHAR(50),
    lastname VARCHAR(50),
    access_token VARCHAR(100),
    refresh_token VARCHAR(100)
);

CREATE TABLE Actividad(
    ID INT NOT NULL PRIMARY KEY,
    IDathlete INT NOT NULL,
    distance FLOAT NOT NULL,
    FOREIGN KEY(IDathlete) REFERENCES Usuario(ID),
    actvity_type VARCHAR(50)

);

CREATE TABLE TipoPregunta(
    tipo VARCHAR(50) NOT NULL PRIMARY KEY
);

CREATE TABLE Pregunta(
    ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    pregunta VARCHAR(300),
    tipo_pregunta VARCHAR(50),
    tipo_respuesta VARCHAR(50),
    FOREIGN KEY(tipo_pregunta) REFERENCES TipoPregunta(tipo)
);

CREATE TABLE Registro(
    id_activity INT NOT NULL,
    id_pregunta INT NOT NULL,
    respuesta VARCHAR(50),
    PRIMARY KEY (id_activity, id_pregunta),
    FOREIGN KEY(id_activity) REFERENCES Actividad(ID),
    FOREIGN KEY(id_pregunta) REFERENCES Pregunta(ID)
);

INSERT INTO Usuario
VALUES
(2, 'DiteR', 'Serprob', 'Pachprob','e72cadb2dd9255e4d61065091539f941033ec2c1', 'f3addde72af00b6a9c6aeb1671ce4bb4104ac852'),
(1231231, 'Pext', 'Cristian', 'Muñoz', 'e69cadb2dd9255e4d61065091539f941033ec2c1', 'f1addde72af00b6a9c6aeb1671ce4bb4104ac852'),
(1, 'pauli', 'Paulina', 'Cardenas', 'e70cadb2dd9255e4d61065091539f941033ec2c1', 'f2addde72af00b6a9c6aeb1671ce4bb4104ac852'),
(3, 'prob', 'prob', 'prob', '1', '2');

INSERT INTO Actividad
VALUES
(123456, 2, 13, "run"),
(1234561, 2, 18, "run"),
(12345623, 2, 14, "jump"),
(12345624, 1, 14, "run"),
(12345625, 1, 37, "run"),
(12345626, 1231231, 28, "jump");

INSERT INTO TipoPregunta
VALUES
("pep"),
("pl"),
("pr");

INSERT INTO Pregunta
VALUES
(1, "Cómo calificaría el nivel de esfuerzo para completar el entrenamiento?", "pep", "slider"),
(2, "¿Cómo calificaría su calidad de sueño la noche anterior al entrenamiento?", "pep", "slider"),
(3, "¿Como calificaria su motivación durante el entrenamiento?", "pep", "slider"),
(4, "¿Cómo calificaría su estrés durante el entrenamiento?","pep", "slider"),
(5, "¿Cómo calificaría su ánimo durante el entrenamiento?", "pep", "slider"),
(6, "¿Cómo calificaría su fatiga en general?", "pep", "slider"),
(11, "¿Lorem ipsum bla bla bla?", "pl", "checkbox"),
(12, "¿Lorem ipsum bla bla bla?", "pl", "slider"),
(13, "¿Lorem ipsum bla bla bla?", "pl", "slider"),
(14, "¿Lorem ipsum bla bla bla?", "pl", "checkbox"),
(15, "¿Lorem ipsum bla bla bla?", "pl", "slider"),
(16, "¿Lorem ipsum bla bla bla?", "pr", "slider"),
(17, "¿Lorem ipsum bla bla bla?", "pr", "checkbox"),
(18, "¿Lorem ipsum bla bla bla?", "pr", "slider"),
(19, "¿Lorem ipsum bla bla bla?", "pr", "slider"),
(20, "¿Lorem ipsum bla bla bla?", "pr", "checkbox");


INSERT INTO Registro
VALUES
(123456, 1, "10"),
(123456, 2, "8"),
(123456, 3, "10"),
(123456, 4, "8"),
(123456, 5, "10"),
(123456, 6, "8"),
(1234561, 2, "3"),
(12345623, 1, "5"),
(12345624, 3, "6"),
(12345625, 3, "5"),
(12345626, 1, "3");