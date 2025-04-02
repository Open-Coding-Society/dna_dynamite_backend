from flask import Flask, jsonify
from api import fetch_trivia_questions  # Import the function
from flask_cors import CORS


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://127.0.0.1:4887"}})

@app.route('/get-questions', methods=['GET'])
def get_questions():
    questions = fetch_trivia_questions()
    return jsonify(questions)

if __name__ == '__main__':
    app.run(debug=True, port=8887)  # Run Flask on port 8887

