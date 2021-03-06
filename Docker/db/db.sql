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
    name_activity VARCHAR(50),
    type_activity VARCHAR(50),
    date_start DATE NOT NULL,
    start_date_local DATE NOT NULL,
    FOREIGN KEY(IDathlete) REFERENCES Usuario(ID)

);

CREATE TABLE TipoCuestionario(
    tipo VARCHAR(50) NOT NULL PRIMARY KEY
);

CREATE TABLE Pregunta(
    ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    pregunta VARCHAR(300),
    tipo_cuestionario VARCHAR(50),
    FOREIGN KEY(tipo_cuestionario) REFERENCES TipoCuestionario(tipo)
);

CREATE TABLE Registro(
    id_activity VARCHAR (50) NOT NULL,
    id_pregunta INT NOT NULL,
    respuesta VARCHAR(200),
    Fecha DATE NOT NULL,
    PRIMARY KEY (id_activity, id_pregunta),
    FOREIGN KEY(id_activity) REFERENCES Actividad(ID),
    FOREIGN KEY(id_pregunta) REFERENCES Pregunta(ID)
);

CREATE TABLE PreguntaSlider(
    id_pregunta INT NOT NULL PRIMARY KEY,
    tipo_respuesta VARCHAR(20),
    tipo_preg VARCHAR(20),
    valueStringMin VARCHAR(50),
    valueStringMax VARCHAR(50),
    FOREIGN KEY(id_pregunta) REFERENCES Pregunta(ID)
);

CREATE TABLE PreguntaDropDown(
    id_pregunta INT NOT NULL,
    tipo_respuesta VARCHAR(20),
    onFocus VARCHAR(20),
    onBlur VARCHAR(20),
    FOREIGN KEY(id_pregunta) REFERENCES Pregunta(ID)
);

CREATE TABLE Alternativas(
    id_pregunta INT NOT NULL,
    alternativa VARCHAR(200),
    FOREIGN KEY(id_pregunta) REFERENCES PreguntaDropDown(id_pregunta)
);

INSERT INTO Usuario
VALUES
(2, 'DiteR', 'Serprob', 'Pachprob','e72cadb2dd9255e4d61065091539f941033ec2c1', 'f3addde72af00b6a9c6aeb1671ce4bb4104ac852'),
(1231231, 'Pext', 'Cristian', 'Mu??oz', 'e69cadb2dd9255e4d61065091539f941033ec2c1', 'f1addde72af00b6a9c6aeb1671ce4bb4104ac852'),
(1, 'pauli', 'Paulina', 'Cardenas', 'e70cadb2dd9255e4d61065091539f941033ec2c1', 'f2addde72af00b6a9c6aeb1671ce4bb4104ac852'),
(3, 'prob', 'prob', 'prob', '1', '2');

INSERT INTO Actividad
VALUES
(123456, 2, 13, 14, 14, 15, 13.2, "caminata", "run", '2022-04-03', '2022-04-03'),
(1234561, 2, 13, 14, 14, 15, 13.2, "caminata", "run", '2022-04-03', '2022-04-03'),
(12345623, 2, 13, 14, 14, 15, 13.2, "caminata", "run", '2022-04-03', '2022-04-03'),
(1234563, 2, 13, 14, 14, 15, 13.2, "caminata", "run", '2022-04-03', '2022-04-03'),
(1234564, 2, 13, 14, 14, 15, 13.2, "caminata", "run", '2022-04-03', '2022-04-03');

INSERT INTO TipoCuestionario
VALUES
("pep"),
("pl"),
("pr"),
("pu");

INSERT INTO Pregunta
VALUES
(1, "??C??mo calificar??a el nivel de esfuerzo para completar el entrenamiento?", "pep"),
(2, "??C??mo calificar??a su calidad de sue??o la noche anterior al entrenamiento?", "pep"),
(3, "??Como calificaria su motivaci??n durante el entrenamiento?", "pep"),
(4, "??C??mo calificar??a su estr??s durante el entrenamiento?","pep"),
(5, "??C??mo calificar??a su ??nimo durante el entrenamiento?", "pep"),
(6, "??C??mo calificar??a su fatiga en general?", "pep"),
(11, "??C??mo se produjo su lesi??n?", "pl"),
(12, "??C??mo fue el inicio de su lesi??n?", "pl"),
(13, "Si el inicio de su lesi??n fue s??bidto, ??Cu??l fue el mecanismo de su lesi??n?", "pl"),
(14, "??En qu?? parte del cuerpo fue su lesi??n?", "pl"),
(15, "??En qu?? tejido fue su lesi??n?", "pl"),
(16, "Creo que me gustar??a usar esta aplicaci??n con frecuencia.", "pu"),
(17, "Encontr?? la aplicaci??n innecesariamente compleja.", "pu"),
(18, "Pens?? que la aplicaci??n era f??cil de usar.", "pu"),
(19, "Creo que necesitar??a el apoyo de un t??cnico para poder utilizar la aplicaci??n.", "pu"),
(20, "Descubr?? que las diversas funciones de este sistema estaban bien integradas.", "pu"),
(21, "Pens?? que hab??a demasiada inconsistencia en este sistema.", "pu"),
(22, "Me imagino que la mayor??a de la gente aprender??a a usar esta aplicaci??n muy r??pidamente", "pu"),
(23, "Encontr?? la aplicaci??n muy engorrosa de usar.", "pu"),
(24, "Me sent?? muy confiado usando la aplicaci??n.", "pu"),
(25, "Necesitaba aprender muchas cosas antes de poder ponerme en marcha con este sistema.", "pu");


INSERT INTO PreguntaDropDown
VALUES
(11, "dropdown", 'blue', 'gray'),
(12, "dropdown", 'blue', 'gray'),
(13, "dropdown", 'blue', 'gray'),
(14, "dropdown", 'blue', 'gray'),
(15, "dropdown", 'blue', 'gray');

INSERT INTO PreguntaSlider
VALUES
(1, "slider", "negativa", "Extremadamente ligero", "Extremadamente duro"),
(2, "slider", "negativa", "Bastante buena", "Bastante mala"),
(3, "slider", "positiva", "Nada motivado", "Muy motivado"),
(4, "slider", "negativa", "Nada de estresado", "Muy estresado"),
(5, "slider", "positiva", "Muy desanimado", "Muy animado"),
(6, "slider", "negativa", "Nada de fatigado", "Muy fatigado"),
(16, "slider", "positiva", "Totalmente en desacuerdo", "Totalmente de acuerdo"),
(17, "slider", "negativa", "Totalmente en desacuerdo", "Totalmente de acuerdo"),
(18, "slider", "positiva", "Totalmente en desacuerdo", "Totalmente de acuerdo"),
(19, "slider", "negativa", "Totalmente en desacuerdo", "Totalmente de acuerdo"),
(20, "slider", "positiva", "Totalmente en desacuerdo", "Totalmente de acuerdo"),
(21, "slider", "negativa", "Totalmente en desacuerdo", "Totalmente de acuerdo"),
(22, "slider", "positiva", "Totalmente en desacuerdo", "Totalmente de acuerdo"),
(23, "slider", "negativa", "Totalmente en desacuerdo", "Totalmente de acuerdo"),
(24, "slider", "positiva", "Totalmente en desacuerdo", "Totalmente de acuerdo"),
(25, "slider", "negativa", "Totalmente en desacuerdo", "Totalmente de acuerdo");


INSERT INTO Registro
VALUES
(123456, 1, "10", '2022-04-03'),
(123456, 2, "8", '2022-04-03'),
(123456, 3, "10", '2022-04-03'),
(123456, 4, "8", '2022-04-03'),
(123456, 5, "10", '2022-04-03'),
(123456, 6, "8", '2022-04-03'),
(1234561, 2, "3", '2022-04-12');

INSERT INTO Alternativas
VALUES
(11, "Corriendo"),
(11, "En otra actividad asociada a correr (entrenamiento, traslados, preparaci??n f??sica, etc.)"),
(11, "Otra actividad no asociada a correr"),
(12, "S??bito, sin molestias anteriores"),
(12, "S??bito, pero con molestias anteriores"),
(12, "Gradual, las molestias incrementaron gradualmente"),
(13, "Sin contacto con un objeto o persona Ejemplo: Lesionarse el tobillo al correr)"),
(13, "Con contacto indirecto con objeto o persona (Ejemplo: Contactar con un objeto y secundariamente lesionarse el tobillo)"),
(13, "Con contacto directo con un objeto o persona (Ejemplo: Golpearse con un objeto directamente en el tobillo, lesion??ndolo)"),
(14, "Cabeza"),
(14, "Cuello"),
(14, "Hombros"),
(14, "Brazo"),
(14, "Codo"),
(14, "Antebrazo"),
(14, "Mu??eca"),
(14, "Manos"),
(14, "Pecho"),
(14, "Columna tor??cica"),
(14, "Columna lumbosacra"),
(14, "Abdomen"),
(14, "Cadera/Ingle"),
(14, "Muslo"),
(14, "Rodilla"),
(14, "Pierna"),
(14, "Tobillo"),
(14, "Pie"),
(15, "M??sculo"),
(15, "Tend??n"),
(15, "Cerebro"),
(15, "M??dula espina"),
(15, "Nervios perif??ricos"),
(15, "Hueso"),
(15, "Cart??lago"),
(15, "Bursa"),
(15, "C??psula"),
(15, "Ligamento"),
(15, "Piel"),
(15, "Vasos"),
(15, "Organos internos");