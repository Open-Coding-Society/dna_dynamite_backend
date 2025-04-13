from flask import Blueprint, Flask, request, jsonify, g
from flask_restful import Api, Resource
from api.jwt_authorize import token_required
from model.gemini import TriviaQuestion
from model.gemini import TriviaResponse  
from model.user import User
from __init__ import app, db
import requests
import os
import json
from dotenv import load_dotenv

gemini_api = Blueprint('gemini_api', __name__, url_prefix='/api')
api = Api(gemini_api)

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

@gemini_api.route("/geneticstrivia", methods=["POST", "GET"])
def get_dna_question():
    """API endpoint to fetch a DNA/genetics trivia question"""
    if request.method == "GET":
        return jsonify(fetch_dna_question())
    else:
        return jsonify({"message": "Use a GET request to generate a DNA/genetics trivia question."})

def fetch_dna_question():
    """Fetches a multiple-choice question about DNA or genetics and stores it in the database"""
    if not GEMINI_API_KEY:
        return {"error": "API Key is missing from .env file"}

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": "Generate a different multiple-choice trivia question about basic biotech/genetics. Provide the question, the answer choices, the correct answer (A, B, C, or D), and an explanation for the correct answer in JSON format. The question key is question, the answer options are answer_options, the correct answer is correct_answer, and the explanation is explanation. DO NOT MAKE THE CORRECT ANSWER C."
                    }
                ]
            }
        ]
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()

        data = response.json()
        text_response = data["candidates"][0]["content"]["parts"][0]["text"]

        # Use regex to extract JSON from markdown block
        import re
        match = re.search(r"```json\s*(\{.*?\})\s*```", text_response, re.DOTALL)
        if not match:
            return {"error": "Gemini did not return valid JSON in the expected format."}

        json_string = match.group(1).strip()
        question_data = json.loads(json_string)

        # Save to database
        trivia = TriviaQuestion(
            question=question_data["question"],
            answer_options=question_data["answer_options"],
            correct_answer=question_data["correct_answer"],
            explanation=question_data["explanation"]
        )
        db.session.add(trivia)
        db.session.commit()

        return trivia.to_dict()

    except requests.exceptions.RequestException as req_err:
        return {"error": f"Request error: {req_err}"}
    except json.JSONDecodeError as json_err:
        return {"error": f"JSON decode error: {json_err}"}
    except Exception as err:
        return {"error": f"Unexpected error: {err}"}

if __name__ == "__main__":
    app.run(debug=True)
    
    
@gemini_api.route("/submit_answer", methods=["POST"])
def submit_answer():
    """Records user's answer and whether it was correct."""
    data = request.get_json()

    question_id = data.get("question_id")
    selected_answer = data.get("selected_answer")

    question = TriviaQuestion.query.get(question_id)
    if not question:
        return jsonify({"error": "Question not found"}), 404

    is_correct = selected_answer.upper() == question.correct_answer.upper()

    response = TriviaResponse(
        question_id=question.id,
        selected_answer=selected_answer.upper(),
        is_correct=is_correct
    )
    db.session.add(response)
    db.session.commit()

    return jsonify({
        "message": "Answer recorded.",
        "is_correct": is_correct,
        "correct_answer": question.correct_answer,
        "explanation": question.explanation
    })


