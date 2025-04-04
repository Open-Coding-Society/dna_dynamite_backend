from flask import Blueprint, Flask, request, jsonify
from flask_restful import Api, Resource
from __init__ import app
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
    """Fetches a multiple-choice question about DNA or genetics"""
    if not GEMINI_API_KEY:
        return {"error": "API Key is missing from .env file"}

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"

    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": "Generate a single multiple-choice trivia question about DNA or genetics with A, B, C, D, answer options. Provide the question, the anwser choices, the correct answer A, B, C, or D, and an explanation for the answer in JSON format. Change the correct answer choice every time. Vary the questions slightly"
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
        if match:
            json_string = match.group(1).strip()
            return json.loads(json_string)
        else:
            return {"error": "Gemini did not return valid JSON in the expected format."}

    except requests.exceptions.RequestException as req_err:
        return {"error": f"Request error: {req_err}"}
    except json.JSONDecodeError as json_err:
        return {"error": f"JSON decode error: {json_err}"}
    except Exception as err:
        return {"error": f"Unexpected error: {err}"}

if __name__ == "__main__":
    app.run(debug=True)

