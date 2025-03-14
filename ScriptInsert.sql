INSERT INTO test_table (id, name) VALUES (1, 'Hola');
INSERT INTO test_table (id, name) VALUES (2, 'Test Name 2');
--INFORMACION DE CLIENTES
INSERT INTO Info_Cliente (id, correo, correo_confirmado, passkey, numero, created_at, updated_at) VALUES (1, 'juan.perez@example.com', 'TRUE', 'passkey123', '555-1234', SYSTIMESTAMP, NULL);
INSERT INTO Info_Cliente (id, correo, correo_confirmado, passkey, numero, created_at, updated_at) VALUES (2, 'jose.perez@example.com', 'FALSE', 'MYPASSS', '*53 1252135556', SYSTIMESTAMP, NULL);
--LUGARES DE ENTREGA
INSERT INTO Lugar_Entrega (id, Numero_Hogar, Nombre_CA, Ciudad_Entrega, Estado_Entrega, Codigo_Postal, created_at, updated_at) VALUES (1, '123', 'Casa de Juan', 'Guadalajara', 'Jalisco', '44100', SYSTIMESTAMP, NULL);
--SKU DE PRODUCTOS
INSERT INTO SKU (id, SKU, Nombre_Producto, Descripccion_Producto, Precio_Producto, created_at, updated_at) VALUES (1, 'SKU123', 'Producto 1', 'Descripccion del Producto 1', 100, SYSTIMESTAMP, NULL);
--SLUGS DE PRODUCTOS
INSERT INTO SLUG (id, SLUD_description, created_at, updated_at) VALUES (1, 'SLUG 1', SYSTIMESTAMP, NULL);
--DEPARTAMENTOS
INSERT INTO DEPARTAMENTO (id, Funcion_Departamento, Nombre_Departamento, created_at, updated_at) VALUES (1, 'Funcion 1', 'Departamento 1', SYSTIMESTAMP, NULL);
--INFORMACION DE TRABAJADORES
INSERT INTO Info_trabajador (id, correo, numero, puesto, created_at, updated_at) VALUES (1, 'ejemplo@correo.com', '1234567890', 'Desarrollador', SYSTIMESTAMP, NULL);
--SEDES
INSERT INTO SEDE (id, Nombre_Sede, created_at, updated_at) VALUES (1, 'Sede 1', SYSTIMESTAMP, NULL);
INSERT INTO SEDE (id, Nombre_Sede, created_at, updated_at) VALUES (2, 'Sede 2', SYSTIMESTAMP, NULL);
--CATEGORIAS
INSERT INTO CATEGORIAS (id, Nombre_Categoria, created_at, updated_at) VALUES (1, 'Categoria 1', SYSTIMESTAMP, NULL);
--CLIENTES
INSERT INTO CLIENTE (id, Documento_nacional, Nombre_Cliente, Apellido_Cliente, Actiivo, created_at, updated_at, id_info_cliente) VALUES (1, '123456', 'Juan', 'Perez', 'TRUE', SYSTIMESTAMP, NULL, 1);
--PRODUCTOS
INSERT INTO PRODUCTO (id, created_at, updated_at, Id_Categoria, id_sku, id_slug) VALUES (1, SYSTIMESTAMP, NULL, 1, 1, 1);
--TRABAJADORES
INSERT INTO TRABAJADORES (id, Documento_nacional, Nombre_Trabajador, Apellido_Trabajador, Actiivo, created_at, updated_at, id_info_trabajador, Id_Sede, Id_Departamento) VALUES (1, '123456', 'Juan', 'Perez', 'TRUE', SYSTIMESTAMP, NULL, 1, 1, 1);
--ORDENES
INSERT INTO ORDENES (id, created_at, updated_at, id_cliente, Id_Sede) VALUES (1, SYSTIMESTAMP, NULL, 1, 1);
--ORDENES ENTREGADAS
INSERT INTO Ordenes_Entregadas (id, company, Estado_de_Entrega, created_at, updated_at, id_orden, id_lugar_entrega) VALUES (1, 'Company 1', 'Entregado', SYSTIMESTAMP, NULL, 1, 1);
--PAGOS
INSERT INTO PAGOS (id, Metodo_pago, created_at, updated_at, id_cliente) VALUES (1, 'Tarjeta', SYSTIMESTAMP, NULL, 1);
--DIRECCIONES
INSERT INTO DIRECCIONES (id, numero_residencia, Nombre_CA, Ciudad, Estado, Codigo_Postal, created_at, updated_at, id_cliente) VALUES (1, '123', 'Casa de Juan', 'Guadalajara', 'Jalisco', '44100', SYSTIMESTAMP, NULL, 1);
--PRODUCTOS DEVOLUCION
INSERT INTO Productos_Devolucion (id, Descripcion, Estado_devolucion, fecha_solicitud, created_at, updated_at, id_producto) VALUES (1, 'Producto defectuoso', 'En proceso', SYSTIMESTAMP, SYSTIMESTAMP, NULL, 1);
--INVENTARIO
INSERT INTO Inventario (id, Cantidad_inventario, created_at, updated_at, id_producto, id_sede) VALUES (1, 100000, SYSTIMESTAMP, NULL, 1, 1);
--IMAGENES
INSERT INTO Imagenes (id, URL, created_at, updated_at, id_producto) VALUES (1, 'http://example.com', SYSTIMESTAMP, NULL, 1);
--PAGO DE ORDENES
INSERT INTO Pago_Ordenes (id, Cantidad_ordenada, precio_orden, created_at, updated_at, id_orden, id_producto) VALUES (1, 1, 100, SYSTIMESTAMP, NULL, 1, 1);
--ORDENES PRODUCTOS
INSERT INTO Ordenes_Productos (id, Cantidad_ordenada, Precio_orden, created_at, updated_at, id_orden, id_producto) VALUES (1, 1, 100, SYSTIMESTAMP, NULL, 1, 1);
--MOVIMIENTOS
INSERT INTO Movimientos (id, fecha_estimada_entrega, fecha_solicitud_entrega, created_at, updated_at, id_sede_origen, id_sede_destino) VALUES (1, SYSTIMESTAMP, SYSTIMESTAMP, SYSTIMESTAMP, NULL, 1, 2);
--MOVIMIENTO PRODUCTOS
INSERT INTO Movimiento_Productos (id, Cantidad_movimiento, created_at, updated_at, id_producto, id_movimiento) VALUES (1, 1, SYSTIMESTAMP, NULL, 1, 1);
COMMIT;
