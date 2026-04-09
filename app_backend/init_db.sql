CREATE DATABASE IF NOT EXISTS prode;
USE prode;

CREATE TABLE IF NOT EXISTS equipo (
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS partido (
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    id_equipo_local INT NOT NULL,
    id_equipo_visitante INT NOT NULL,
    estadio VARCHAR(150)  NOT NULL,
    ciudad VARCHAR(200)  NOT NULL,
    fecha_partido DATETIME NOT NULL,
    fase_torneo ENUM('grupos','dieciseisavos','octavos','cuartos','semis','final') NOT NULL,
    goles_local INT,
    goles_visitante INT,
    FOREIGN KEY (id_equipo_local) REFERENCES equipo(id),
    FOREIGN KEY (id_equipo_visitante) REFERENCES equipo(id)
);

CREATE TABLE IF NOT EXISTS usuario (
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    nombre_usuario VARCHAR(150) NOT NULL UNIQUE,
    email VARCHAR(150) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS prediccion (
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    id_usuario INT,
    id_partido INT,
    goles_local INT NOT NULL,
    goles_visitante INT NOT NULL,
    FOREIGN KEY (id_usuario) REFERENCES usuario(id),
    FOREIGN KEY (id_partido) REFERENCES partido(id),
    UNIQUE (id_usuario, id_partido)
);

CREATE TABLE IF NOT EXISTS ranking (
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    id_usuario INT UNIQUE,
    puntos_usuario INT,
    FOREIGN KEY (id_usuario) REFERENCES usuario(id)
);


INSERT INTO equipo (nombre) VALUES ('ARGENTINA');
INSERT INTO equipo (nombre) VALUES ('BRASIL');
INSERT INTO equipo (nombre) VALUES ('ALEMANIA');
INSERT INTO equipo (nombre) VALUES ('FRANCIA');

INSERT INTO partido (id_equipo_local, id_equipo_visitante, estadio, ciudad, fecha_partido, fase_torneo, goles_local, goles_visitante)
VALUES (1, 2, 'Hard Rock Stadium', 'Miami', '2026-08-12 07:30:00','final', NULL, NULL);
INSERT INTO partido (id_equipo_local, id_equipo_visitante, estadio, ciudad, fecha_partido, fase_torneo, goles_local, goles_visitante)
VALUES (1, 3, 'hola', 'londres', '2025-09-12 07:30:00','final', NULL, NULL);

INSERT INTO usuario (nombre_usuario, email) VALUES ('azul10', 'azulita@gmail.com');
INSERT INTO usuario (nombre_usuario, email) VALUES ('amarillito', 'amarillito@gmail.com');
INSERT INTO usuario (nombre_usuario, email) VALUES ('violetita', 'violetita@gmail.com');


/* PRUEBA DEL UNIQUE*/
INSERT INTO prediccion (id_usuario, id_partido, goles_local, goles_visitante) VALUES (1, 1, 10, 2);
INSERT INTO prediccion (id_usuario, id_partido, goles_local, goles_visitante) VALUES (3, 2, 10, 2);


