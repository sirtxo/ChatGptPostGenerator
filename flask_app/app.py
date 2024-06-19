from flask import Flask, request, jsonify, abort
from flask_cors import CORS
from functools import wraps
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

# Función para obtener un valor de configuración de la tabla configuration
def get_configuration_value(key):
    query = "SELECT config_value FROM configuration WHERE config_key = %s"
    result = fetch_query(query, (key,))
    if result:
        return result[0]['config_value']
    else:
        raise ValueError(f"{key} not found in configuration table")

# Decorador para validar la API key
def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('x-api-key')
        stored_api_key = get_configuration_value('api_key')
        if api_key and api_key == stored_api_key:
            return f(*args, **kwargs)
        else:
            abort(401)
    return decorated_function

# Ruta para agregar una pregunta
@app.route('/api/questions', methods=['POST'])
@require_api_key
def post_question():
    data = request.get_json()

    # Obtener la clave de API de OpenAI desde la base de datos
    openai_api_key = get_configuration_value('openai_api_key')
    openai.api_key = openai_api_key

    # Obtener la respuesta de ChatGPT
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a wise and knowledgeable genie who provides insightful and magical answers to questions."},
            {"role": "user", "content": data['message']}
        ],
        max_tokens=150
    )
    gpt_response = "Question Genie GPT te dice: " + response.choices[0].message['content'].strip()

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
