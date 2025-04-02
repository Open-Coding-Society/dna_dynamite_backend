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
                        "text": "Generate 5 multiple-choice trivia questions with 4 options each. Provide the correct answer in a structured JSON format."
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

        # Convert string to Python dictionary
        trivia_data = json.loads(text_response)

        return trivia_data  # Return properly formatted JSON

    except requests.exceptions.HTTPError as http_err:
        return {"error": f"HTTP error occurred: {http_err}"}
    except Exception as err:
        return {"error": f"Other error occurred: {err}"}

# Example usage
trivia_questions = fetch_trivia_questions()
print(json.dumps(trivia_questions, indent=2))
