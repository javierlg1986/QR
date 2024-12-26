CREATE TABLE usuarios (
    id INTEGER PRIMARY KEY,
    usuario VARCHAR(254) PRIMARY KEY,
    administrador INTEGER, 
    nombre_completo VARCHAR(254),
    pass VARCHAR(24),
    bloqueado INTEGER,
    permiso INTEGER, 
    diestro INTEGER,
    token VARCHAR(8)
);

CREATE TABLE log_accesos (
    id INTEGER PRIMARY KEY,
    fecha INTEGER,
    id_usuario INTEGER,
    url TEXT,
    exito BOOLEAN,
    ip TEXT,
    FOREIGN KEY(id_usuario) REFERENCES usuarios(id)
);

CREATE TABLE log_cambios (
    id INTEGER PRIMARY KEY,
    id_usuario INTEGER,
    fecha INTEGER,
    tabla VARCHAR(254),
    id_tabla INTEGER,
    tipo VARCHAR(2),
    cambio TEXT,
    FOREIGN KEY(id_usuario) REFERENCES usuarios(id)
);

CREATE TABLE parameters (
    id INTEGER PRIMARY KEY,
    label VARCHAR(254),
    family VARCHAR(254)
);

CREATE TABLE QR (
    id INTEGER PRIMARY KEY,
    tokenQR VARCHAR(254) UNIQUE,
    fecha INTEGER,
    id_usuario INTEGER,
    tabla_asignada INTEGER,
    id_elem_en_tabla_asig INTEGER,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id)
    FOREIGN KEY (id_elem_en_tabla_asig) REFERENCES lista_tablas(id)
);

CREATE TABLE lista_tablas (
    id INTEGER PRIMARY KEY,
    nombre_tabla VARCHAR(254) UNIQUE
);

CREATE TABLE Tabla_1 (
    id INTEGER PRIMARY KEY,
    campo_1 VARCHAR(254),
    campo_2 VARCHAR(254),
    campo_3 REAL,
    campo_4 REAL
);

CREATE TABLE Tabla_2 (
    id INTEGER PRIMARY KEY,
    campo_1 VARCHAR(254),
    campo_2 VARCHAR(254),
    campo_3 REAL,
    campo_4 REAL
);

CREATE TABLE Tabla_3 (
    id INTEGER PRIMARY KEY,
    campo_1 VARCHAR(254),
    campo_2 VARCHAR(254),
    campo_3 REAL,
    campo_4 REAL,
    campo_5 REAL
);


-- CREATE TABLE traballos (
--     id INTEGER PRIMARY KEY,
--     expediente VARCHAR(24),
--     cliente VARCHAR(254),
--     enderezo VARCHAR(254),
--     poboacion VARCHAR(254),
--     latitud FLOAT,
--     longitud FLOAT,
--     fecha TIMESTAMP,
--     observacions_int TEXT,
--     observacions_ext TEXT,
--     id_usuario INTEGER,
--     id_estado INTEGER DEFAULT 1,
--     FOREIGN KEY (id_usuario) REFERENCES usuarios(id)
--     FOREIGN KEY (id_estado) REFERENCES parameters(id)
-- );
