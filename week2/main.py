import os
import sys

from dotenv import load_dotenv
from google import genai

# Load API key from .env file
load_dotenv()

# Create Gemini client
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))


def prompt_model(model: str, prompt: str) -> str:
    """Send a prompt to Gemini and return the response text."""
    try:
        response = client.models.generate_content(
            model=model,
            contents=prompt,
        )
        return response.text

    except Exception as error:
        return f"[Gemini Error] {error}"


def main():
    # Check if user provided model and prompt
    if len(sys.argv) < 3:
        print('Usage: uv run prompt_model.py <model> "<prompt>"')
        return

    model = sys.argv[1]
    prompt = " ".join(sys.argv[2:])

    response = prompt_model(model, prompt)

    print("--- RESPONSE ---")
    print(response)


if __name__ == "__main__":
    main()