from flask import Flask, jsonify
from flask_cors import CORS
from api import fetch_trivia_questions  # Import the function

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend access

@app.route('/get-questions', methods=['GET'])
def get_questions():
    questions = fetch_trivia_questions()
    return jsonify(questions)

if __name__ == '__main__':
    app.run(debug=True, port=5000)  # Run on port 5000
