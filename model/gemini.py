from flask import Flask, jsonify
from __init__ import app
from gemini import fetch_trivia_questions  # Import the function
from flask_cors import CORS

@app.route('/get-questions', methods=['GET'])
def get_questions():
    questions = fetch_trivia_questions()
    
    # Ensure we always return JSON
    if isinstance(questions, dict):
        return jsonify(questions)
    else:
        return jsonify({"error": "Invalid response from API"}), 500  # Return an error if API response is not JSON

if __name__ == '__main__':
    app.run(debug=True, port=8887)  # Run Flask on port 8887
