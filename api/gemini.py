from flask import Blueprint, request, jsonify
import os
from dotenv import load_dotenv
from google import genai

# Load environment variables
load_dotenv()

# Initialize client with API key from .env
client = genai.Client(api_key=os.getenv("API_KEY"))

# Creating a blueprint for the Gemini API
gemini_api = Blueprint('gemini_api', __name__, url_prefix='/api/gemini')

# POST method to generate content using Gemini
@gemini_api.route('', methods=['POST'])
def generate_content():
    """
    Endpoint to generate AI-generated content using Gemini.
    """
    data = request.get_json()
    prompt = data.get("prompt")

    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash", contents=prompt
        )
        return jsonify({"response": response.text}), 200
    except Exception as e:
        return jsonify({"error": f"Failed to generate content: {str(e)}"}), 500
