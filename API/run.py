from flask import Flask, jsonify, request
import oracledb
import os
import bcrypt

app = Flask(__name__)

# Configuración de la conexión a la base de datos Oracle XE
def get_db_connection():
    dsn = oracledb.makedsn("localhost", 1521, service_name="XEPDB1")
    conn = oracledb.connect(user="SYSTEM", password="202109705", dsn=dsn)
    return conn

@app.route('/api/users/', methods=['POST'])
def create_user():
    data = request.json

    required_fields = ["Documento_nacional", "Nombre_Cliente", "Apellido_Cliente", "correo", "password", "numero"]
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Datos incompletos'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Verificar si el correo ya existe
        cursor.execute("SELECT id FROM Info_Cliente WHERE correo = :correo", {'correo': data["correo"]})
        if cursor.fetchone():
            return jsonify({'error': 'El correo ya está registrado'}), 409

        # Hashear la contraseña con bcrypt
        hashed_password = bcrypt.hashpw(data["password"].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        # Obtener el siguiente ID para Info_Cliente
        cursor.execute("SELECT info_cliente_seq.NEXTVAL FROM DUAL")
        info_id = cursor.fetchone()[0]

        # Insertar en Info_Cliente
        cursor.execute("""
            INSERT INTO Info_Cliente (id, correo, correo_confirmado, passkey, numero, created_at) 
            VALUES (:id, :correo, 'NO', :passkey, :numero, SYSTIMESTAMP)
        """, {'id': info_id, 'correo': data["correo"], 'passkey': hashed_password, 'numero': data["numero"]})

        # Obtener el siguiente ID para CLIENTE
        cursor.execute("SELECT cliente_seq.NEXTVAL FROM DUAL")
        cliente_id = cursor.fetchone()[0]

        # Insertar en CLIENTE
        cursor.execute("""
            INSERT INTO CLIENTE (id, Documento_nacional, Nombre_Cliente, Apellido_Cliente, Actiivo, created_at, id_info_cliente) 
            VALUES (:id, :Documento_nacional, :Nombre_Cliente, :Apellido_Cliente, 'SI', SYSTIMESTAMP, :id_info_cliente)
        """, {'id': cliente_id, 'Documento_nacional': data["Documento_nacional"], 'Nombre_Cliente': data["Nombre_Cliente"], 'Apellido_Cliente': data["Apellido_Cliente"], 'id_info_cliente': info_id})

        conn.commit()

        return jsonify({"status": "success", "message": "User created successfully"}), 201

    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()
        conn.close()

# Endpoint para obtener datos del test por ID
@app.route('/api/test/:<int:id>', methods=['GET'])
def get_cliente(id):
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    SELECT 
        c.id, c.Nombre_Cliente, c.Apellido_Cliente, ic.correo, ic.numero, c.created_at
    FROM CLIENTE c
    LEFT JOIN Info_Cliente ic ON c.id_info_cliente = ic.id
    WHERE c.id = :id
    """

    cursor.execute(query, {'id': id})
    result = cursor.fetchone()

    cursor.close()
    conn.close()

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

if __name__ == '__main__':
    app.run(debug=True)