from flask import Flask, jsonify, request
import oracledb
import os

app = Flask(__name__)

# Configuración de la conexión a la base de datos Oracle XE
def get_db_connection():
    dsn = oracledb.makedsn("localhost", 1521, service_name="XEPDB1")
    conn = oracledb.connect(user="SYSTEM", password="202109705", dsn=dsn)
    return conn

# Endpoint para obtener datos del test por ID
@app.route('/api/test/<int:id>', methods=['GET'])
def get_test_by_id(id):
    # Verificar si hay autenticación, por ejemplo usando una cookie (opcional)

    conn = get_db_connection()
    cursor = conn.cursor()

    # Realizar la consulta SQL para obtener los datos de la tabla
    cursor.execute("SELECT id, name FROM test_table WHERE id = :id", {'id': id})
    result = cursor.fetchone()

    cursor.close()
    conn.close()

    if result is None:
        return jsonify({'error': 'Not Found'}), 404

    return jsonify({'id': result[0], 'name': result[1]}), 200

if __name__ == '__main__':
    app.run(debug=True)