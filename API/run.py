from flask import Flask, jsonify, request
import oracledb
import os
import bcrypt

app = Flask(__name__)

# Conexión a la base de datos
def get_db_connection():
    dsn = oracledb.makedsn("localhost", 1521, service_name="XEPDB1")
    conn = oracledb.connect(user="SYSTEM", password="202109705", dsn=dsn)
    return conn

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>CLIENTES/USUARIOS<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
# Crear nuevo cliente
@app.route('/api/users/', methods=['POST'])
def create_cliente():
    data = request.json

    required_fields = ["Documento_nacional", "Nombre_Cliente", "Apellido_Cliente", "correo", "correo_confirmado", "password", "numero"]
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Datos incompletos'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Verificar si el correo o el documento nacional ya están registrados
        cursor.execute("SELECT id FROM Info_Cliente WHERE correo = :correo", {'correo': data["correo"]})
        if cursor.fetchone():
            return jsonify({'error': 'El correo ya está registrado'}), 409
            
        cursor.execute("SELECT id FROM CLIENTE WHERE Documento_nacional = :doc", {'doc': data["Documento_nacional"]})
        if cursor.fetchone():
            return jsonify({'error': 'El Documento_nacional ya está registrado'}), 409

        # Hash de la contraseña
        hashedpass = bcrypt.hashpw(data["password"].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        # Obtener el siguiente ID para Info_Cliente
        cursor.execute("SELECT info_cliente_seq.NEXTVAL FROM DUAL")
        info_id = cursor.fetchone()[0]

        # Insertar en Info_Cliente
        cursor.execute("""
            INSERT INTO Info_Cliente (id, correo, correo_confirmado, passkey, numero, created_at) 
            VALUES (:id, :correo, :correo_confirmado, :passkey, :numero, SYSTIMESTAMP)
        """, {'id': info_id, 'correo': data["correo"], 'correo_confirmado': data["correo_confirmado"], 'passkey': hashedpass, 'numero': data["numero"]})

        # Obtener el siguiente ID para CLIENTE
        cursor.execute("SELECT cliente_seq.NEXTVAL FROM DUAL")
        cliente_id = cursor.fetchone()[0]

        # Insertar en CLIENTE con Actiivo = 'TRUE' por defecto
        cursor.execute("""
            INSERT INTO CLIENTE (id, Documento_nacional, Nombre_Cliente, Apellido_Cliente, Actiivo, created_at, id_info_cliente) 
            VALUES (:id, :Documento_nacional, :Nombre_Cliente, :Apellido_Cliente, 'TRUE', SYSTIMESTAMP, :id_info_cliente)
        """, {'id': cliente_id, 'Documento_nacional': data["Documento_nacional"], 'Nombre_Cliente': data["Nombre_Cliente"], 'Apellido_Cliente': data["Apellido_Cliente"], 'id_info_cliente': info_id})

        conn.commit()

        return jsonify({"status": "Exitoso", "message": "Cliente creado de forma exitosa"}), 201

    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()
        conn.close()

#Login de clientes (Correo y contraseña)
@app.route('/api/users/login', methods=['POST'])
def login_cliente():
    data = request.json

    required_fields = ["correo", "password"]
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Datos incompletos'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT id, passkey FROM Info_Cliente WHERE correo = :correo", {'correo': data["correo"]})
        result = cursor.fetchone()

        if result is None:
            return jsonify({'error': 'Credenciales inválidas'}), 401

        user_id, stored_passkey = result

        if stored_passkey.startswith("$2b$"):  # Verifica si es un hash bcrypt
            password_correct = bcrypt.checkpw(data["password"].encode('utf-8'), stored_passkey.encode('utf-8'))
        else:  # Si no es hash, comparar directamente
            password_correct = data["password"] == stored_passkey

        if password_correct:
            return jsonify({"status": "Exitoso", "message": "Inicio de sesión exitoso", "user_id": user_id}), 200
        else:
            return jsonify({"error": "Credenciales inválidas"}), 401

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()
        conn.close()

# Obtener Cliente por ID
@app.route('/api/users/:<int:id>', methods=['GET'])
def get_cliente(id):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        query = """
        SELECT 
            c.id, c.Nombre_Cliente, c.Apellido_Cliente, ic.correo, ic.numero, c.created_at, c.Actiivo
        FROM CLIENTE c
        LEFT JOIN Info_Cliente ic ON c.id_info_cliente = ic.id
        WHERE c.id = :id
        """

        cursor.execute(query, {'id': id})
        result = cursor.fetchone()

        if result is None or result[6] == 'FALSE':  # Validamos si el cliente no existe o está inactivo
            return jsonify({'error': 'Usuario no encontrado'}), 404

        response = {
            "id": result[0],
            "Nombre Cliente": result[1],
            "Apellido Cliente": result[2],
            "correo": result[3],
            "numero": result[4],
            "CreatedAt": result[5].isoformat() if result[5] else None
        }

        return jsonify(response), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()
        conn.close()

# Actualizar Cliente por ID
@app.route('/api/users/:<int:id>', methods=['PUT'])
def update_cliente(id):
    data = request.json

    required_fields = ["correo", "numero"]
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Datos inválidos'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Obtener el ID correcto de Info_Cliente a partir de CLIENTE
        cursor.execute("SELECT id_info_cliente FROM CLIENTE WHERE id = :id", {'id': id})
        result = cursor.fetchone()

        if not result:
            return jsonify({'error': 'Cliente no existe'}), 404

        id_info_cliente = result[0]

        # Actualizar Info_Cliente
        cursor.execute("""
            UPDATE Info_Cliente
            SET correo = :correo, numero = :numero
            WHERE id = :id_info_cliente
        """, {'correo': data["correo"], 'numero': data["numero"], 'id_info_cliente': id_info_cliente})

        conn.commit()

        return jsonify({"status": "Exitoso", "message": "Cliente actualizado de forma exitosa"}), 200

    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()
        conn.close()

# Eliminar Cliente por ID
@app.route('/api/users/:<int:id>', methods=['DELETE'])
def deactivate_cliente(id):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Verificar si el cliente existe y su estado
        cursor.execute("SELECT Actiivo FROM CLIENTE WHERE id = :id", {'id': id})
        result = cursor.fetchone()

        if not result:
            return jsonify({'error': 'Cliente no encontrado'}), 404

        estado_actual = result[0]

        # Si ya está inactivo, devolver 404 como si no existiera
        if estado_actual == 'FALSE':
            return jsonify({'error': 'Cliente no encontrado'}), 404

        # Actualizar el estado a inactivo
        cursor.execute("""
            UPDATE CLIENTE
            SET Actiivo = 'FALSE'
            WHERE id = :id
        """, {'id': id})

        conn.commit()

        return jsonify({"status": "Exitoso", "message": "Cliente desactivado correctamente"}), 200

    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()
        conn.close()

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>PRODUCTOS<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
# Crear nuevo producto
@app.route('/api/products/', methods=['POST'])
def create_producto():
    data = request.json

    required_fields = ["sku", "nombre_producto", "descripcion_producto", "precio_producto", "descripcion_slug", "id_categoria"]
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Datos incompletos'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT id FROM CATEGORIAS WHERE id = :id_categoria", {'id_categoria': data["id_categoria"]})
        if not cursor.fetchone():
            return jsonify({'error': 'Categoría no encontrada'}), 404

        cursor.execute("SELECT id FROM SKU WHERE SKU = :sku", {'sku': data["sku"]})
        if cursor.fetchone():
            return jsonify({'error': 'El SKU ingresado ya existe'}), 409

        cursor.execute("SELECT sku_seq.NEXTVAL FROM DUAL")
        sku_id = cursor.fetchone()[0]

        cursor.execute("""
            INSERT INTO SKU (id, SKU, Nombre_Producto, Descripccion_Producto, Precio_Producto, created_at, updated_at) 
            VALUES (:id, :sku, :nombre, :descripcion, :precio, SYSTIMESTAMP, SYSTIMESTAMP)
        """, {
            'id': sku_id,
            'sku': data["sku"],  
            'nombre': data["nombre_producto"],
            'descripcion': data["descripcion_producto"],
            'precio': data["precio_producto"]
        })

        cursor.execute("SELECT slug_seq.NEXTVAL FROM DUAL")
        slug_id = cursor.fetchone()[0]

        cursor.execute("""
            INSERT INTO SLUG (id, SLUD_description, created_at, updated_at) 
            VALUES (:id, :descripcion, SYSTIMESTAMP, SYSTIMESTAMP)
        """, {
            'id': slug_id,
            'descripcion': data["descripcion_slug"]
        })

        cursor.execute("SELECT producto_seq.NEXTVAL FROM DUAL")
        producto_id = cursor.fetchone()[0]

        cursor.execute("""
            INSERT INTO PRODUCTO (id, created_at, updated_at, id_categoria, id_sku, id_slug, activo) 
            VALUES (:id, SYSTIMESTAMP, SYSTIMESTAMP, :id_categoria, :id_sku, :id_slug, 'TRUE')
        """, {
            'id': producto_id,
            'id_categoria': data["id_categoria"],
            'id_sku': sku_id,
            'id_slug': slug_id
        })

        conn.commit()

        return jsonify({
            "status": "Exitoso",
            "message": "Producto creado exitosamente",
            "id_producto": producto_id,
            "id_sku": sku_id,
            "sku": data["sku"],
            "id_slug": slug_id
        }), 201

    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()
        conn.close()

#Listar productos
@app.route('/api/products/', methods=['GET'])
def get_all_productos():
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        query = """
        SELECT 
            p.id, s.SKU, s.Nombre_Producto, s.Descripccion_Producto, s.Precio_Producto, 
            c.Nombre_Categoria, sl.SLUD_description, 
            p.created_at, p.updated_at
        FROM PRODUCTO p
        JOIN SKU s ON p.id_sku = s.id
        JOIN CATEGORIAS c ON p.id_categoria = c.id
        JOIN SLUG sl ON p.id_slug = sl.id
        WHERE p.activo = 'TRUE'
        """

        cursor.execute(query)
        results = cursor.fetchall()

        if not results:
            return jsonify({'message': 'No hay productos registrados'}), 200

        productos = []
        for result in results:
            productos.append({
                "id_producto": result[0],
                "sku": result[1],
                "nombre_producto": result[2],
                "descripcion_producto": result[3],
                "precio_producto": result[4],
                "categoria": result[5],
                "slug": result[6],
                "created_at": result[7].isoformat() if result[7] else None,
                "updated_at": result[8].isoformat() if result[8] else None
            })

        return jsonify(productos), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()
        conn.close()

#Buscar producto por ID
@app.route('/api/products/:<int:id>', methods=['GET'])
def get_producto_by_id(id):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        query = """
        SELECT 
            p.id, s.SKU, s.Nombre_Producto, s.Descripccion_Producto, s.Precio_Producto, 
            c.Nombre_Categoria, sl.SLUD_description, 
            p.created_at, p.updated_at, p.activo
        FROM PRODUCTO p
        JOIN SKU s ON p.id_sku = s.id
        JOIN CATEGORIAS c ON p.id_categoria = c.id
        JOIN SLUG sl ON p.id_slug = sl.id
        WHERE p.id = :id
        """

        cursor.execute(query, {'id': id})
        result = cursor.fetchone()

        if result is None:
            return jsonify({'error': 'Producto no encontrado'}), 404

        if result[9] == 'FALSE':  
            return jsonify({'error': 'Este producto no está disponible'}), 404

        response = {
            "id_producto": result[0],
            "sku": result[1],
            "nombre_producto": result[2],
            "descripcion_producto": result[3],
            "precio_producto": result[4],
            "categoria": result[5],
            "slug": result[6],
            "created_at": result[7].isoformat() if result[7] else None,
            "updated_at": result[8].isoformat() if result[8] else None
        }

        return jsonify(response), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()
        conn.close()

#Actualizar producto por ID
@app.route('/api/products/:<int:id>', methods=['PUT'])
def update_producto(id):
    data = request.json

    required_fields = ["precio_producto", "id_categoria"]
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Datos incompletos'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # 🔹 Verificar si el producto existe
        cursor.execute("SELECT id_sku FROM PRODUCTO WHERE id = :id", {'id': id})
        result = cursor.fetchone()

        if result is None:
            return jsonify({'error': 'Producto no encontrado'}), 404

        id_sku = result[0]  # Obtener el id_sku del producto

        # 🔹 Verificar si la nueva categoría existe
        cursor.execute("SELECT id FROM CATEGORIAS WHERE id = :id_categoria", {'id_categoria': data["id_categoria"]})
        if not cursor.fetchone():
            return jsonify({'error': 'Categoría no encontrada'}), 404

        # 🔹 Actualizar el precio en la tabla SKU
        cursor.execute("""
            UPDATE SKU 
            SET Precio_Producto = :precio_producto, updated_at = SYSTIMESTAMP 
            WHERE id = :id_sku
        """, {'precio_producto': data["precio_producto"], 'id_sku': id_sku})

        # 🔹 Actualizar la categoría en la tabla PRODUCTO
        cursor.execute("""
            UPDATE PRODUCTO 
            SET id_categoria = :id_categoria, updated_at = SYSTIMESTAMP 
            WHERE id = :id
        """, {'id_categoria': data["id_categoria"], 'id': id})

        conn.commit()

        return jsonify({
            "status": "Exitoso",
            "message": "Producto actualizado correctamente"
        }), 200

    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()
        conn.close()

#Eliminar producto por ID
Disable = {}
@app.route('/api/products/:<int:id>', methods=['DELETE'])
def delete_producto(id):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # 🔹 Verificar si el producto existe
        cursor.execute("SELECT id FROM PRODUCTO WHERE id = :id", {'id': id})
        if not cursor.fetchone():
            return jsonify({'error': 'Producto no encontrado'}), 404

        # 🔹 Marcar el producto como eliminado lógicamente
        cursor.execute("""
            UPDATE PRODUCTO 
            SET activo = 'FALSE', updated_at = SYSTIMESTAMP 
            WHERE id = :id
        """, {'id': id})

        conn.commit()

        return jsonify({
            "status": "Exitoso",
            "message": "Producto marcado como eliminado lógicamente"
        }), 200

    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()
        conn.close()
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>ORDENES<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
# Crear nueva orden
@app.route('/api/orders/', methods=['POST'])
def create_pago_orden():
    data = request.json

    required_fields = ["id_orden", "cantidad_ordenada", "id_producto"]
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Datos incompletos'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT id FROM ORDENES WHERE id = :id_orden", {'id_orden': data["id_orden"]})
        if not cursor.fetchone():
            return jsonify({'error': 'Orden no encontrada'}), 404

        cursor.execute("""
            SELECT s.Precio_Producto 
            FROM SKU s 
            JOIN PRODUCTO p ON p.id_sku = s.id 
            WHERE p.id = :id_producto
        """, {'id_producto': data["id_producto"]})

        producto = cursor.fetchone()

        if not producto:
            return jsonify({'error': 'Producto no encontrado'}), 404

        precio_producto = producto[0]
        precio_total = data["cantidad_ordenada"] * precio_producto

        cursor.execute("SELECT pago_ord.NEXTVAL FROM DUAL")
        pago_orden_id = cursor.fetchone()[0]

        cursor.execute("""
            INSERT INTO Pago_Ordenes (id, Cantidad_ordenada, precio_orden, created_at, id_orden, id_producto) 
            VALUES (:id, :cantidad_ordenada, :precio_orden, SYSTIMESTAMP, :id_orden, :id_producto)
        """, {
            'id': pago_orden_id,
            'cantidad_ordenada': data["cantidad_ordenada"],
            'precio_orden': precio_producto,
            'id_orden': data["id_orden"], 
            'id_producto': data["id_producto"]
        })

        conn.commit()

        return jsonify({
            "status": "Exitoso",
            "message": "Pago de orden creado de forma exitosa",
            "id_pago_orden": pago_orden_id,
            "precio_total": precio_total
        }), 201

    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()
        conn.close()

# Obtener Ordenes de pago
@app.route('/api/orders/', methods=['GET'])
def list_pago_ordenes():
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # 🔹 Consultar todas las órdenes de pago con información del producto
        query = """
        SELECT 
            po.id, po.id_orden, po.id_producto, po.Cantidad_ordenada, po.precio_orden, 
            s.Nombre_Producto, (po.Cantidad_ordenada * po.precio_orden) AS precio_total,
            po.created_at, po.updated_at
        FROM Pago_Ordenes po
        JOIN PRODUCTO p ON po.id_producto = p.id
        JOIN SKU s ON p.id_sku = s.id
        ORDER BY po.created_at DESC
        """

        cursor.execute(query)
        results = cursor.fetchall()

        if not results:
            return jsonify({'message': 'No hay órdenes de pago registradas'}), 200

        ordenes = []
        for result in results:
            ordenes.append({
                "id_pago_orden": result[0],
                "id_orden": result[1],
                "id_producto": result[2],
                "cantidad_ordenada": result[3],
                "precio_unitario": result[4],
                "nombre_producto": result[5],
                "precio_total": result[6],
                "created_at": result[7].isoformat() if result[7] else None,
                "updated_at": result[8].isoformat() if result[8] else None
            })

        return jsonify(ordenes), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()
        conn.close()
# Obtener Orden por ID
@app.route('/api/orders/:<int:id>', methods=['GET'])
def get_pago_orden(id):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # 🔹 Consultar la orden de pago junto con información del producto
        query = """
        SELECT 
            po.id, po.id_orden, po.id_producto, po.Cantidad_ordenada, po.precio_orden, 
            s.Nombre_Producto, (po.Cantidad_ordenada * po.precio_orden) AS precio_total,
            po.created_at, po.updated_at
        FROM Pago_Ordenes po
        JOIN PRODUCTO p ON po.id_producto = p.id
        JOIN SKU s ON p.id_sku = s.id
        WHERE po.id = :id
        """

        cursor.execute(query, {'id': id})
        result = cursor.fetchone()

        if result is None:
            return jsonify({'error': 'Orden no encontrada'}), 404

        response = {
            "id_pago_orden": result[0],
            "id_orden": result[1],
            "id_producto": result[2],
            "cantidad_ordenada": result[3],
            "precio_unitario": result[4],
            "nombre_producto": result[5],
            "precio_total": result[6],
            "created_at": result[7].isoformat() if result[7] else None,
            "updated_at": result[8].isoformat() if result[8] else None
        }

        return jsonify(response), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()
        conn.close()

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>PAGOS<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
# Crear nuevo pago
@app.route('/api/payments/', methods=['POST'])
def create_pago():
    data = request.json

    required_fields = ["id_cliente", "monto", "Metodo_pago"]
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Datos incompletos'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT id FROM CLIENTE WHERE id = :id_cliente", {'id_cliente': data["id_cliente"]})
        if not cursor.fetchone():
            return jsonify({'error': 'Cliente no encontrado'}), 404

        cursor.execute("SELECT pago_seq.NEXTVAL FROM DUAL")
        pago_id = cursor.fetchone()[0]

        cursor.execute("""
            INSERT INTO PAGOS (id, Metodo_pago, created_at, id_cliente) 
            VALUES (:id, :Metodo_pago, SYSTIMESTAMP, :id_cliente)
        """, {'id': pago_id, 'Metodo_pago': data["Metodo_pago"], 'id_cliente': data["id_cliente"]})

        conn.commit()

        return jsonify({
            "status": "Exitoso",
            "message": "Pago creado de forma exitosa",
            "id_pago": pago_id
        }), 201

    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()
        conn.close()

# Obtener Pago por ID
@app.route('/api/payments/', methods=['GET'])
def get_pagos():
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        query = """
        SELECT 
            p.id, p.Metodo_pago, p.created_at, c.Nombre_Cliente, c.Apellido_Cliente
        FROM PAGOS p
        LEFT JOIN CLIENTE c ON p.id_cliente = c.id
        """

        cursor.execute(query)
        results = cursor.fetchall()

        pagos = []
        for result in results:
            pagos.append({
                "id": result[0],
                "Metodo de Pago": result[1],
                "CreatedAt": result[2].isoformat() if result[2] else None,
                "Nombre Cliente": result[3],
                "Apellido Cliente": result[4]
            })

        return jsonify(pagos), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()
        conn.close()
        
if __name__ == '__main__':
    app.run(debug=True)