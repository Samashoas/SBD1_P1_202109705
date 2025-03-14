DROP TABLE test_table;
CREATE TABLE test_table (
    id NUMBER PRIMARY KEY,
    name VARCHAR2(50)
);

DROP TABLE Info_Cliente;
CREATE TABLE Info_Cliente (
    id NUMBER PRIMARY KEY,
    correo VARCHAR2(50) NOT NULL, 
    correo_confirmado VARCHAR(10) NOT NULL,
    passkey VARCHAR2(20) NOT NULL,
    numero VARCHAR2(20) NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP
);

DROP TABLE Lugar_Entrega;
CREATE TABLE Lugar_Entrega(
    id NUMBER PRIMARY KEY,
    Numero_Hogar VARCHAR2(20) NOT NULL,
    Nombre_CA VARCHAR2(50) NOT NULL,
    Ciudad_Entrega VARCHAR2(50) NOT NULL,
    Estado_Entrega VARCHAR2(50) NOT NULL,
    Codigo_Postal VARCHAR2(10) NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP
);

DROP TABLE SKU;
CREATE TABLE SKU(
    id NUMBER PRIMARY KEY,
    SKU VARCHAR2(20) NOT NULL,
    Nombre_Producto VARCHAR2(50) NOT NULL,
    Descripccion_Producto VARCHAR2(100) NOT NULL,
    Precio_Producto NUMBER NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP
);

DROP TABLE SLUG;
CREATE TABLE SLUG(
    id NUMBER PRIMARY KEY,
    SLUD_description VARCHAR2(100) NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP
);

DROP TABLE DEPARTAMENTO;
CREATE TABLE DEPARTAMENTO(
    id NUMBER PRIMARY KEY,
    Funcion_Departamento VARCHAR2(50) NOT NULL,
    Nombre_Departamento VARCHAR2(50) NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP
);

DROP TABLE SEDE;
CREATE TABLE SEDE(
    id NUMBER PRIMARY KEY,
    Nombre_Sede VARCHAR2(50) NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP
);

DROP TABLE CATEGORIAS;
CREATE TABLE CATEGORIAS(
    id NUMBER PRIMARY KEY,
    Nombre_Categoria VARCHAR2(50) NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP
);


INSERT INTO test_table (id, name) VALUES (1, 'Hola');
INSERT INTO test_table (id, name) VALUES (3, 'Test Name 2');
--INFORMACION DE CLIENTES
INSERT INTO Info_Cliente (id, correo, correo_confirmado, passkey, numero, created_at, updated_at) VALUES (1, 'juan.perez@example.com', 'TRUE', 'passkey123', '555-1234', SYSTIMESTAMP, NULL);
INSERT INTO Info_Cliente (id, correo, correo_confirmado, passkey, numero, created_at, updated_at) VALUES (2, 'jose.perez@example.com', 'FALSE', 'MYPASSS', '*53 1252135556', SYSTIMESTAMP, NULL);
--LUGARES DE ENTREGA
INSERT INTO Lugar_Entrega (id, Numero_Hogar, Nombre_CA, Ciudad_Entrega, Estado_Entrega, Codigo_Postal, created_at, updated_at) VALUES (7, '123', 'Casa de Juan', 'Guadalajara', 'Jalisco', '44100', SYSTIMESTAMP, NULL);
--SKU DE PRODUCTOS
INSERT INTO SKU (id, SKU, Nombre_Producto, Descripccion_Producto, Precio_Producto, created_at, updated_at) VALUES (9, 'SKU123', 'Producto 1', 'Descripccion del Producto 1', 100, SYSTIMESTAMP, NULL);
--SLUGS DE PRODUCTOS
INSERT INTO SLUG (id, SLUD_description, created_at, updated_at) VALUES (12, 'SLUG 1', SYSTIMESTAMP, NULL);
--DEPARTAMENTOS
INSERT INTO DEPARTAMENTO (id, Funcion_Departamento, Nombre_Departamento, created_at, updated_at) VALUES (1, 'Funcion 1', 'Departamento 1', SYSTIMESTAMP, NULL);
--SEDES
INSERT INTO SEDE (id, Nombre_Sede, created_at, updated_at) VALUES (3, 'Sede 1', SYSTIMESTAMP, NULL);
INSERT INTO SEDE (id, Nombre_Sede, created_at, updated_at) VALUES (4, 'Sede 2', SYSTIMESTAMP, NULL);
--CATEGORIAS
INSERT INTO CATEGORIAS (id, Nombre_Categoria, created_at, updated_at) VALUES (14, 'Categoria 1', SYSTIMESTAMP, NULL);

COMMIT;

SELECT * FROM test_table;
SELECT * FROM Info_Cliente;
SELECT * FROM Lugar_Entrega;
SELECT * FROM SKU;
SELECT * FROM SLUG;
SELECT * FROM DEPARTAMENTO;
SELECT * FROM SEDE;
SELECT * FROM CATEGORIAS;