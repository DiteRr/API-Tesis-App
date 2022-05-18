CREATE DATABASE stravadb;

USE stravadb;

CREATE TABLE Usuario(
    ID VARCHAR(50) NOT NULL PRIMARY KEY,
    username VARCHAR(50),
    firstname VARCHAR(50),
    lastname VARCHAR(50),
    access_token VARCHAR(100),
    refresh_token VARCHAR(100)
);

CREATE TABLE Actividad(
    ID VARCHAR(50) NOT NULL PRIMARY KEY,
    IDathlete VARCHAR(50) NOT NULL,
    distance FLOAT NOT NULL,
    elapsed_time FLOAT NOT NULL,
    elev_high FLOAT NOT NULL,
    elev_low FLOAT NOT NULL,
    average_speed FLOAT NOT NULL,
    name_activIty VARCHAR(50),
    type_activity VARCHAR(50),
    FOREIGN KEY(IDathlete) REFERENCES Usuario(ID)

);

CREATE TABLE TipoCuestionario(
    tipo VARCHAR(50) NOT NULL PRIMARY KEY
);

CREATE TABLE Pregunta(
    ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    pregunta VARCHAR(300),
    tipo_cuestionario VARCHAR(50),
    tipo_respuesta VARCHAR(100),
    FOREIGN KEY(tipo_cuestionario) REFERENCES TipoCuestionario(tipo)
);

CREATE TABLE Registro(
    id_activity VARCHAR (50) NOT NULL,
    id_pregunta INT NOT NULL,
    respuesta VARCHAR(200),
    PRIMARY KEY (id_activity, id_pregunta),
    FOREIGN KEY(id_activity) REFERENCES Actividad(ID),
    FOREIGN KEY(id_pregunta) REFERENCES Pregunta(ID)
);

CREATE TABLE Alternativas(
    id_pregunta INT NOT NULL,
    alternativa VARCHAR(200),
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
(123456, 2, 13, 14, 14, 15, 13.2, "caminata", "run"),
(1234561, 2, 13, 14, 14, 15, 13.2, "caminata", "run"),
(12345623, 2, 13, 14, 14, 15, 13.2, "caminata", "run"),
(1234563, 2, 13, 14, 14, 15, 13.2, "caminata", "run"),
(1234564, 2, 13, 14, 14, 15, 13.2, "caminata", "run");

INSERT INTO TipoCuestionario
VALUES
("pep"),
("pl"),
("pr");

INSERT INTO Pregunta
VALUES
(1, "¿Como calificaria el nivel de esfuerzo para completar el entrenamiento?", "pep", "slider"),
(2, "¿Como calificaria su calidad de sueño la noche anterior al entrenamiento?", "pep", "slider"),
(3, "¿Como calificaria su motivacion durante el entrenamiento?", "pep", "slider"),
(4, "¿Como calificaria su estres durante el entrenamiento?","pep", "slider"),
(5, "¿Como calificaria su animo durante el entrenamiento?", "pep", "slider"),
(6, "¿Como calificaria su fatiga en general?", "pep", "slider"),
(11, "¿Como se produjo su lesion?", "pl", "dropdown"),
(12, "¿Como fue el inicio de su lesion?", "pl", "dropdown"),
(13, "Si el inicio de su lesion fue subidto, ¿Cuál fue el mecanismo de su lesion?", "pl", "dropdown"),
(14, "¿En que parte del cuerpo fue su lesion?", "pl", "dropdown"),
(15, "¿En que tejido fue su lesion?", "pl", "dropdown"),
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
(1234561, 2, "3");

INSERT INTO Alternativas
VALUES
(11, "Corriendo"),
(11, "En otra actividad asociada a correr (entrenamiento, traslados, preparación fisica, etc.)"),
(11, "Otra actividad no asociada a correr"),
(12, "Subito, sin molestias anteriores"),
(12, "Subito, pero con molestias anteriores"),
(12, "Gradual, las molestias incrementaron gradualmente"),
(13, "Sin contacto con un objeto o persona Ejemplo: Lesionarse el tobillo al correr)"),
(13, "Con contacto indirecto con objeto o persona (Ejemplo: Contactar con un objeto y secundariamente lesionarse el tobillo)"),
(13, "Con contacto directo con un objeto o persona (Ejemplo: Golpearse con un objeto directamente en el tobillo, lesionandolo)"),
(14, "Cabeza"),
(14, "Cuello"),
(14, "Hombros"),
(14, "Brazo"),
(14, "Codo"),
(14, "Antebrazo"),
(14, "Muñeca"),
(14, "Manos"),
(14, "Pecho"),
(14, "Columna toracica"),
(14, "Columna lumbosacra"),
(14, "Abdomen"),
(14, "Cadera/Ingle"),
(14, "Muslo"),
(14, "Rodilla"),
(14, "Pierna"),
(14, "Tobillo"),
(15, "Músculo"),
(15, "Tendon"),
(15, "Cerebro"),
(15, "Médula espina"),
(15, "Hueso"),
(15, "Cartilago"),
(15, "Bursa"),
(15, "Cápsula"),
(15, "Ligamento"),
(15, "Piel"),
(15, "Vasos"),
(15, "Organos internos");