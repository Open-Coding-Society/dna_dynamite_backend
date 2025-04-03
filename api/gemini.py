import requests
import os
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def fetch_trivia_questions():
    if not GEMINI_API_KEY:
        return {"error": "API Key is missing from .env file"}

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"

    headers = {
        "Content-Type": "application/json"
    }

    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": "Generate 5 multiple-choice trivia questions with 4 options each about DNA. Provide the correct answer in a structured JSON format."
                    }
                ]
            }
        ]
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # Raises an HTTPError for bad responses

        data = response.json()
        
        # Extract JSON string from the response
        text_response = data["candidates"][0]["content"]["parts"][0]["text"]
        
        # Remove Markdown-style JSON formatting (```json ... ```)
        if text_response.startswith("```json"):
            text_response = text_response[7:-3].strip()

        # Convert string to Python dictionary safely
        try:
            trivia_data = json.loads(text_response)
        except json.JSONDecodeError:
            return {"error": "Failed to parse response as JSON"}

        return trivia_data  # Return properly formatted JSON

    except requests.exceptions.RequestException as req_err:
        return {"error": f"Request error: {req_err}"}
    except Exception as err:
        return {"error": f"Unexpected error: {err}"}

