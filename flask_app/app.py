from flask import Flask, request, jsonify
from flask_cors import CORS
import pymysql
from datetime import datetime
import openai

app = Flask(__name__)
CORS(app)  # Permitir CORS para todas las rutas

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


# Función para obtener el token de la tabla configuration
def get_openai_api_key():
    query = "SELECT config_value FROM configuration WHERE config_key = %s"
    result = fetch_query(query, ('openai_api_key',))
    if result:
        return result[0]['config_value']
    else:
        raise ValueError("OpenAI API key not found in configuration table")


# Ruta para agregar una pregunta
@app.route('/api/questions', methods=['POST'])
def post_question():
    data = request.get_json()

    # Obtener la clave de API de OpenAI desde la base de datos
    openai_api_key = get_openai_api_key()
    openai.api_key = openai_api_key

    # Obtener la respuesta de ChatGPT
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": data['message']}
        ],
        max_tokens=150
    )
    gpt_response =  "Question Genie GPT te dice: " + response.choices[0].message['content'].strip()

    # Insertar la pregunta y la respuesta en la base de datos
    query = """
        INSERT INTO questions (name, message, response, timestamp)
        VALUES (%s, %s, %s, %s)
    """
    timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    lastrowid = execute_query(query, (data['name'], data['message'], gpt_response, timestamp))

    return jsonify({
        'id': lastrowid,
        'name': data['name'],
        'message': data['message'],
        'response': gpt_response,
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
