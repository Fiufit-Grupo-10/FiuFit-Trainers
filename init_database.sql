CREATE TABLE users (
    uid VARCHAR(50) UNIQUE PRIMARY KEY,
    email VARCHAR(100) UNIQUE,
    username VARCHAR(50) UNIQUE,
    birthday DATE,
    height INTEGER,
    weight INTEGER,
    gender VARCHAR(1),
    target VARCHAR,
    level VARCHAR,
    latitude INTEGER,
    longitude INTEGER,
    user_type VARCHAR(7)
);

CREATE TABLE trainingtypes (
    name VARCHAR(50) PRIMARY KEY UNIQUE,
    descr TEXT
);

CREATE TABLE user_trainingtype (
    username VARCHAR REFERENCES users(username),
    trainingtype VARCHAR REFERENCES trainingtypes(name),
    PRIMARY KEY (username, trainingtype)
);

CREATE TABLE admins (
    uid VARCHAR(50) UNIQUE PRIMARY KEY,
    email VARCHAR(100) UNIQUE,
    username VARCHAR(50) UNIQUE
);

INSERT INTO trainingtypes VALUES 
('Cardio','Entrenamientos relacionados a la resistencia aerobica'), 
('Fuerza','Entrenamientos relacionados a ganar fuerza'), 
('HIIT','Entrenamientos HIIT'),
 ('Tonificación','Entrenamientos relacionados a tonificar los músculos'), 
 ('Baile','Entrenamientos con musica'),
 ('Kickboxing','Entrenamientos de pelea'), 
 ('Pilates','Entrenamientos de pilates'),
 ('Mediatación','Entrenamientos de meditación'),
 ('Estirar','Entrenamientos de estiramiento'),
 ('Yoga','Entrenamientos de Yoga'),
 ('Spinning','Entrenamientos de spinning'),
 ('Cinta','Entrenamientos de cinta');