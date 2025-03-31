import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def fetch_trivia_questions():
    if not GEMINI_API_KEY:
        return {"error": "API Key is missing from .env file"}

    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key"  # Replace with the correct URL from Gemini API documentation

    headers = {
        "Authorization": f"Bearer {GEMINI_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "prompt": "Generate 5 multiple-choice trivia questions with 4 options each. Provide the correct answer. Format the response in JSON.",
        "max_tokens": 500
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # Raises an HTTPError if the response was not successful

        # If API responds with an error
        if response.status_code != 200:
            return {"error": f"API Error: {response.status_code}, {response.text}"}

        return response.json()  # Return the JSON response if everything is fine
    except requests.exceptions.HTTPError as http_err:
        return {"error": f"HTTP error occurred: {http_err}"}
    except Exception as err:
        return {"error": f"Other error occurred: {err}"}

# Example usage:
if __name__ == "__main__":
    trivia_questions = fetch_trivia_questions()
    print(trivia_questions)
