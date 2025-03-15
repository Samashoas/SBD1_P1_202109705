--Deshabilita las claves foraneas en caso de que existan en alguna tabla y no hagan conflicto
--Elmina llave foranea CLIENTE
ALTER TABLE CLIENTE DROP CONSTRAINT fk_info_cliente;

ALTER TABLE PRODUCTO DROP CONSTRAINT fk_categoria;
ALTER TABLE PRODUCTO DROP CONSTRAINT fk_sku;
ALTER TABLE PRODUCTO DROP CONSTRAINT fk_slug;

ALTER TABLE TRABAJADORES DROP CONSTRAINT fk_info_trabajador;
ALTER TABLE TRABAJADORES DROP CONSTRAINT fk_sede;
ALTER TABLE TRABAJADORES DROP CONSTRAINT fk_departamento;

ALTER TABLE ORDENES DROP CONSTRAINT fk_cliente;
ALTER TABLE ORDENES DROP CONSTRAINT fk_sede_orden;

ALTER TABLE Ordenes_Entregadas DROP CONSTRAINT fk_orden;
ALTER TABLE Ordenes_Entregadas DROP CONSTRAINT fk_lugar_entrega;

ALTER TABLE PAGOS DROP CONSTRAINT fk_cliente_pago;

ALTER TABLE DIRECCIONES DROP CONSTRAINT fk_cliente_direccion;

ALTER TABLE Productos_Devolucion DROP CONSTRAINT fk_producto_devolucion;

ALTER TABLE Inventario DROP CONSTRAINT fk_producto_inventario;
ALTER TABLE Inventario DROP CONSTRAINT fk_sede_inventario;


ALTER TABLE Imagenes DROP CONSTRAINT fk_producto_imagen;

ALTER TABLE Pago_Ordenes DROP CONSTRAINT fk_orden_pago;
ALTER TABLE Pago_Ordenes DROP CONSTRAINT fk_producto_pago;

ALTER TABLE Ordenes_Productos DROP CONSTRAINT fk_orden_producto;
ALTER TABLE Ordenes_Productos DROP CONSTRAINT fk_producto_orden;

ALTER TABLE Movimientos DROP CONSTRAINT fk_sede_origen;
ALTER TABLE Movimientos DROP CONSTRAINT fk_sede_destino;

ALTER TABLE Movimiento_Productos DROP CONSTRAINT fk_producto_movimiento;
ALTER TABLE Movimiento_Productos DROP CONSTRAINT fk_movimiento_producto;



DROP TABLE test_table;
CREATE TABLE test_table (
    id NUMBER PRIMARY KEY,
    name VARCHAR2(50)
);

DROP SEQUENCE info_cliente_seq;
DROP TABLE Info_Cliente;
CREATE TABLE Info_Cliente (
    id NUMBER PRIMARY KEY,
    correo VARCHAR2(50) NOT NULL, 
    correo_confirmado VARCHAR(10) NOT NULL,
    passkey VARCHAR2(255) NOT NULL,
    numero VARCHAR2(20) NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP
);
CREATE SEQUENCE info_cliente_seq START WITH 10 INCREMENT BY 1;

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

DROP SEQUENCE sku_seq;
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
CREATE SEQUENCE sku_seq START WITH 10 INCREMENT BY 1;

DROP SEQUENCE slug_seq;
DROP TABLE SLUG;
CREATE TABLE SLUG(
    id NUMBER PRIMARY KEY,
    SLUD_description VARCHAR2(100) NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP
);
CREATE SEQUENCE slug_seq START WITH 10 INCREMENT BY 1;

DROP TABLE DEPARTAMENTO;
CREATE TABLE DEPARTAMENTO(
    id NUMBER PRIMARY KEY,
    Funcion_Departamento VARCHAR2(50) NOT NULL,
    Nombre_Departamento VARCHAR2(50) NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP
);

DROP TABLE Info_trabajador;
CREATE TABLE Info_trabajador(
    id NUMBER PRIMARY KEY,
    correo VARCHAR2(50) NOT NULL,
    numero VARCHAR2(20) NOT NULL,
    puesto VARCHAR2(50) NOT NULL,
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

DROP SEQUENCE cliente_seq;
DROP TABLE CLIENTE;
CREATE TABLE CLIENTE(
    id NUMBER PRIMARY KEY,
    Documento_nacional VARCHAR2(20) NOT NULL,
    Nombre_Cliente VARCHAR2(50) NOT NULL,
    Apellido_Cliente VARCHAR2(50) NOT NULL,
    Actiivo VARCHAR(10) NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP,
    id_info_cliente NUMBER
);
ALTER TABLE CLIENTE ADD CONSTRAINT fk_info_cliente FOREIGN KEY (id_info_cliente) REFERENCES Info_Cliente(id);
CREATE SEQUENCE cliente_seq START WITH 10 INCREMENT BY 1;

DROP SEQUENCE producto_seq;
DROP TABLE PRODUCTO;
CREATE TABLE PRODUCTO(
    id NUMBER PRIMARY KEY,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP,
    Id_Categoria NUMBER,
    id_sku NUMBER,
    id_slug NUMBER
);
ALTER TABLE PRODUCTO ADD CONSTRAINT fk_categoria FOREIGN KEY (Id_Categoria) REFERENCES CATEGORIAS(id);
ALTER TABLE PRODUCTO ADD CONSTRAINT fk_sku FOREIGN KEY (id_sku) REFERENCES SKU(id);
ALTER TABLE PRODUCTO ADD CONSTRAINT fk_slug FOREIGN KEY (id_slug) REFERENCES SLUG(id);
CREATE SEQUENCE producto_seq START WITH 10 INCREMENT BY 1;

DROP TABLE TRABAJADORES;
CREATE TABLE TRABAJADORES(
    id NUMBER PRIMARY KEY,
    Documento_nacional VARCHAR2(20) NOT NULL,
    Nombre_Trabajador VARCHAR2(50) NOT NULL,
    Apellido_Trabajador VARCHAR2(50) NOT NULL,
    Actiivo VARCHAR(10) NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP,
    id_info_trabajador NUMBER,
    Id_Sede NUMBER,
    Id_Departamento NUMBER
);
ALTER TABLE TRABAJADORES ADD CONSTRAINT fk_info_trabajador FOREIGN KEY (id_info_trabajador) REFERENCES Info_trabajador(id);
ALTER TABLE TRABAJADORES ADD CONSTRAINT fk_sede FOREIGN KEY (Id_Sede) REFERENCES SEDE(id);
ALTER TABLE TRABAJADORES ADD CONSTRAINT fk_departamento FOREIGN KEY (Id_Departamento) REFERENCES DEPARTAMENTO(id);

DROP TABLE ORDENES;
CREATE TABLE ORDENES(
    id NUMBER PRIMARY KEY,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP,
    id_cliente NUMBER,
    Id_Sede NUMBER
);
ALTER TABLE ORDENES ADD CONSTRAINT fk_cliente FOREIGN KEY (id_cliente) REFERENCES CLIENTE(id);
ALTER TABLE ORDENES ADD CONSTRAINT fk_sede_orden FOREIGN KEY (Id_Sede) REFERENCES SEDE(id);

DROP TABLE Ordenes_Entregadas;
CREATE TABLE Ordenes_Entregadas(
    id NUMBER PRIMARY KEY,
    company VARCHAR2(50) NOT NULL,
    Estado_de_Entrega VARCHAR2(50) NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP,
    id_orden NUMBER,
    id_lugar_entrega NUMBER
);
ALTER TABLE Ordenes_Entregadas ADD CONSTRAINT fk_orden FOREIGN KEY (id_orden) REFERENCES ORDENES(id);
ALTER TABLE Ordenes_Entregadas ADD CONSTRAINT fk_lugar_entrega FOREIGN KEY (id_lugar_entrega) REFERENCES Lugar_Entrega(id);

DROP SEQUENCE pago_seq;
DROP TABLE PAGOS;
CREATE TABLE PAGOS(
    id NUMBER PRIMARY KEY,
    Metodo_pago VARCHAR2(50) NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP,
    id_cliente NUMBER
);
ALTER TABLE PAGOS ADD CONSTRAINT fk_cliente_pago FOREIGN KEY (id_cliente) REFERENCES CLIENTE(id);
CREATE SEQUENCE pago_seq START WITH 10 INCREMENT BY 1;

DROP TABLE DIRECCIONES;
CREATE TABLE DIRECCIONES(
    id NUMBER PRIMARY KEY,
    numero_residencia VARCHAR2(20) NOT NULL,
    Nombre_CA VARCHAR2(50) NOT NULL,
    Ciudad VARCHAR2(50) NOT NULL,
    Estado VARCHAR2(50) NOT NULL,
    Codigo_Postal VARCHAR2(10) NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP,
    id_cliente NUMBER
);
ALTER TABLE DIRECCIONES ADD CONSTRAINT fk_cliente_direccion FOREIGN KEY (id_cliente) REFERENCES CLIENTE(id);

DROP TABLE Productos_Devolucion;
CREATE TABLE Productos_Devolucion(
    id NUMBER PRIMARY KEY,
    Descripcion VARCHAR2(100) NOT NULL,
    Estado_devolucion VARCHAR2(50) NOT NULL,
    fecha_solicitud timestamp NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP,
    id_producto NUMBER
);
ALTER TABLE Productos_Devolucion ADD CONSTRAINT fk_producto_devolucion FOREIGN KEY (id_producto) REFERENCES PRODUCTO(id);

DROP TABLE Inventario;
CREATE TABLE Inventario(
    id NUMBER PRIMARY KEY,
    Cantidad_inventario NUMBER NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP,
    id_producto NUMBER,
    id_sede NUMBER
);
ALTER TABLE Inventario ADD CONSTRAINT fk_producto_inventario FOREIGN KEY (id_producto) REFERENCES PRODUCTO(id);
ALTER TABLE Inventario ADD CONSTRAINT fk_sede_inventario FOREIGN KEY (id_sede) REFERENCES SEDE(id);

DROP TABLE Imagenes;
CREATE TABLE Imagenes(
    id NUMBER PRIMARY KEY,
    URL VARCHAR2(100) NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP,
    id_producto NUMBER
);
ALTER TABLE Imagenes ADD CONSTRAINT fk_producto_imagen FOREIGN KEY (id_producto) REFERENCES PRODUCTO(id);

DROP SEQUENCE pago_order;
DROP TABLE Pago_Ordenes;
CREATE TABLE Pago_Ordenes(
    id NUMBER PRIMARY KEY,
    Cantidad_ordenada NUMBER NOT NULL,
    precio_orden NUMBER NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP,
    id_orden NUMBER,
    id_producto NUMBER
);
ALTER TABLE Pago_Ordenes ADD CONSTRAINT fk_orden_pago FOREIGN KEY (id_orden) REFERENCES ORDENES(id);
ALTER TABLE Pago_Ordenes ADD CONSTRAINT fk_producto_pago FOREIGN KEY (id_producto) REFERENCES PRODUCTO(id);
CREATE SEQUENCE pago_order START WITH 10 INCREMENT BY 1;

DROP TABLE Ordenes_Productos;
CREATE TABLE Ordenes_Productos(
    id NUMBER PRIMARY KEY,
    Cantidad_ordenada NUMBER NOT NULL,
    Precio_orden NUMBER NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP,
    id_orden NUMBER,
    id_producto NUMBER
);
ALTER TABLE Ordenes_Productos ADD CONSTRAINT fk_orden_producto FOREIGN KEY (id_orden) REFERENCES ORDENES(id);
ALTER TABLE Ordenes_Productos ADD CONSTRAINT fk_producto_orden FOREIGN KEY (id_producto) REFERENCES PRODUCTO(id);

DROP TABLE Movimientos;
CREATE TABLE Movimientos(
    id NUMBER PRIMARY KEY,
    fecha_estimada_entrega TIMESTAMP NOT NULL,
    fecha_solicitud_entrega TIMESTAMP NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP,
    id_sede_origen NUMBER,
    id_sede_destino NUMBER
);
ALTER TABLE Movimientos ADD CONSTRAINT fk_sede_origen FOREIGN KEY (id_sede_origen) REFERENCES SEDE(id);
ALTER TABLE Movimientos ADD CONSTRAINT fk_sede_destino FOREIGN KEY (id_sede_destino) REFERENCES SEDE(id);

DROP TABLE Movimiento_Productos;
CREATE TABLE Movimiento_Productos(
    id NUMBER PRIMARY KEY,
    Cantidad_movimiento NUMBER NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP,
    id_producto NUMBER,
    id_movimiento NUMBER
);
ALTER TABLE Movimiento_Productos ADD CONSTRAINT fk_producto_movimiento FOREIGN KEY (id_producto) REFERENCES PRODUCTO(id);
ALTER TABLE Movimiento_Productos ADD CONSTRAINT fk_movimiento_producto FOREIGN KEY (id_movimiento) REFERENCES Movimientos(id);