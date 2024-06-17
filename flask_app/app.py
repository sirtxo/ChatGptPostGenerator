from flask import Flask, request, jsonify
import pymysql
from datetime import datetime

app = Flask(__name__)

# Configuración de la base de datos
DATABASE_CONFIG = {
    'host': 'mariadb',
    'user': 'user',
    'password': 'password',
    'db': 'questiongenuine',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

# Función para ejecutar consultas de escritura (INSERT, UPDATE, DELETE)
def execute_query(query, args=()):
    connection = pymysql.connect(**DATABASE_CONFIG)
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, args)
            connection.commit()
            return cursor.lastrowid
    finally:
        connection.close()

# Función para ejecutar consultas de lectura (SELECT)
def fetch_query(query, args=()):
    connection = pymysql.connect(**DATABASE_CONFIG)
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, args)
            result = cursor.fetchall()
            return result
    finally:
        connection.close()

# Ruta para agregar una pregunta
@app.route('/api/questions', methods=['POST'])
def post_question():
    data = request.get_json()
    query = """
        INSERT INTO questions (name, message, response, timestamp)
        VALUES (%s, %s, %s, %s)
    """
    timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    response = data.get('response', "")
    lastrowid = execute_query(query, (data['name'], data['message'], response, timestamp))
    return jsonify({
        'id': lastrowid,
        'name': data['name'],
        'message': data['message'],
        'response': response,
        'timestamp': timestamp
    }), 201

# Ruta para obtener todas las preguntas
@app.route('/api/questions', methods=['GET'])
def get_questions():
    query = "SELECT id, name, message, response, timestamp FROM questions"
    questions = fetch_query(query)
    return jsonify(questions), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
