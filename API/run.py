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
def create_user():
    data = request.json

    required_fields = ["Documento_nacional", "Nombre_Cliente", "Apellido_Cliente", "correo", "correo_confirmado", "password", "numero", "activo"]
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Datos incompletos'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Verificar si la inforamción ya está registrada en info_Clientes y Clientes
        cursor.execute("SELECT id FROM Info_Cliente WHERE correo = :correo", {'correo': data["correo"]})
        if cursor.fetchone():
            return jsonify({'error': 'El correo ya está registrado'}), 409
            
        cursor.execute("SELECT id FROM CLIENTE WHERE Documento_nacional = :doc", {'doc': data["Documento_nacional"]})
        if cursor.fetchone():
            return jsonify({'error': 'El Documento_nacional ya está registrado'}), 409

        # Hash de la contraseña
        hashedpass = bcrypt.hashpw(data["password"].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        cursor.execute("SELECT info_cliente_seq.NEXTVAL FROM DUAL")
        info_id = cursor.fetchone()[0]

        cursor.execute("""
            INSERT INTO Info_Cliente (id, correo, correo_confirmado, passkey, numero, created_at) 
            VALUES (:id, :correo, :correo_confirmado, :passkey, :numero, SYSTIMESTAMP)
        """, {'id': info_id, 'correo': data["correo"], 'correo_confirmado': data["correo_confirmado"], 'passkey': hashedpass, 'numero': data["numero"]})

        cursor.execute("SELECT cliente_seq.NEXTVAL FROM DUAL")
        cliente_id = cursor.fetchone()[0]

        cursor.execute("""
            INSERT INTO CLIENTE (id, Documento_nacional, Nombre_Cliente, Apellido_Cliente, Actiivo, created_at, id_info_cliente) 
            VALUES (:id, :Documento_nacional, :Nombre_Cliente, :Apellido_Cliente, :activo, SYSTIMESTAMP, :id_info_cliente)
        """, {'id': cliente_id, 'Documento_nacional': data["Documento_nacional"], 'Nombre_Cliente': data["Nombre_Cliente"], 'Apellido_Cliente': data["Apellido_Cliente"], 'activo': data["activo"], 'id_info_cliente': info_id})

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
@app.route('/api/test/:<int:id>', methods=['GET'])
def get_cliente(id):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        query = """
        SELECT 
            c.id, c.Nombre_Cliente, c.Apellido_Cliente, ic.correo, ic.numero, c.created_at
        FROM CLIENTE c
        LEFT JOIN Info_Cliente ic ON c.id_info_cliente = ic.id
        WHERE c.id = :id
        """

        cursor.execute(query, {'id': id})
        result = cursor.fetchone()

        if result is None:
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

if __name__ == '__main__':
    app.run(debug=True)