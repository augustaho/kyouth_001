from google import genai
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Create Gemini client using API key from .env
client = genai.Client(
    api_key=os.getenv("GOOGLE_API_KEY")
)


# Function to send a prompt to Gemini and return the response
def prompt_model(model: str, prompt: str) -> str:

    try:
        # Send prompt to selected Gemini model
        response = client.models.generate_content(
            model=model,
            contents=prompt
        )

        # Return generated text
        return response.text

    except Exception as e:
        # Return error message instead of crashing
        return f"Error: {e}"