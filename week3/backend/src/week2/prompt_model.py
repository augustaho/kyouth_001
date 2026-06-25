import os
import sys
import requests
from dotenv import load_dotenv
from google import genai

# Load environment variables from .env file
load_dotenv()

# Create Gemini client using API key from .env
gemini_client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))


def call_gemini(model: str, prompt: str) -> str:
    """Send prompt to Gemini and return the response."""

    try:
        response = gemini_client.models.generate_content(
            model=model,
            contents=prompt,
        )

        return response.text

    except Exception as error:
        return f"[Gemini Error] {error}"


def call_ollama(model: str, prompt: str) -> str:
    """Send prompt to Ollama local LLM and return the response."""

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": model,
                "prompt": prompt,
                "stream": False,
            },
            timeout=120,
        )

        response.raise_for_status()

        data = response.json()

        return data.get("response", "")

    except Exception as error:
        return f"[Ollama Error] {error}"


def prompt_model(model: str, prompt: str) -> str:
    """
    Choose which LLM to use based on the model name.

    Examples:
    - gemini-1.5-flash  -> Gemini API
    - llama3.1          -> Ollama local LLM
    """

    # If model name contains "gemini", use Google Gemini
    if "gemini" in model.lower():
        return call_gemini(model, prompt)

    # Otherwise, use Ollama
    return call_ollama(model, prompt)


def main():
    """Allow user to choose model and send prompt from terminal."""

    if len(sys.argv) < 3:
        print('Usage: uv run python prompt_model.py <model> "<prompt>"')
        print('Example Gemini: uv run python prompt_model.py gemini-1.5-flash "Explain Python"')
        print('Example Ollama: uv run python prompt_model.py llama3.1 "Explain Python"')
        return

    model = sys.argv[1]
    prompt = " ".join(sys.argv[2:])

    response = prompt_model(model, prompt)

    print("--- RESPONSE ---")
    print(response)


if __name__ == "__main__":
    main()