from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory storage for questions
questions = []

@app.route('/api/questions', methods=['POST'])
def post_question():
    data = request.get_json()
    question = {
        'id': len(questions) + 1,
        'question': data['question']
    }
    questions.append(question)
    return jsonify(question), 201

@app.route('/api/questions', methods=['GET'])
def get_questions():
    return jsonify(questions), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
