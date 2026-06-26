# Week 3: System Integration & Application

## Project Overview

This project builds a full-stack Resume Helper chatbot application. The purpose of the system is to allow users to interact with an AI-powered backend through a simple web interface.

The application is separated into two main services:

* **Frontend**: Displays the chatbot page, accepts user messages, and sends requests to the backend.
* **Backend**: Receives chat requests, calls the Week 2 AI function, and returns the AI-generated response.

The system integrates the Week 2 `prompt_model.py` function, which supports both local LLM usage through Ollama and cloud-based Gemini models.

## Setup Instructions

### Prerequisites

Make sure the following tools are installed:

* Python 3.14
* uv
* Docker Desktop
* Docker Compose
* Ollama, if using local LLM models such as `llama3.1:latest`

### Environment Variables

The project uses `.env` files to avoid hardcoding configuration values.

Frontend `.env`:

```env
BACKEND_URL=http://127.0.0.1:8001
```

Backend `.env`:

```env
GOOGLE_API_KEY=your_google_api_key_here
```

The frontend `.env` tells the frontend where the backend server is located. The backend `.env` stores the Gemini API key. The API key is not placed in the frontend because it should not be exposed to users.

### Manual Local Setup

Run the backend:

```bash
cd week3/backend
uv run uvicorn --app-dir src app:app --reload --port 8001
```

Run the frontend in another terminal:

```bash
cd week3/frontend
uv run uvicorn --app-dir src app:app --reload
```

Access the frontend at:

```text
http://127.0.0.1:8000
```

Access the backend API documentation at:

```text
http://127.0.0.1:8001/docs
```

## Usage

The user opens the frontend page and types a message into the chatbot input box. When the user clicks the **Send** button, the frontend sends a JSON request to the backend `/chat` endpoint.

Example user input:

```text
Tell me a joke
```

Example backend response:

```json
{
  "response": "Here is a joke..."
}
```

The frontend then displays the response inside the chat history area.

The Day 1 test page is preserved at:

```text
http://127.0.0.1:8000/hello
```

## API / Function Reference

### POST `/chat`

The backend exposes a `POST /chat` endpoint.

Expected JSON payload:

```json
{
  "message": "Tell me a joke",
  "model": "llama3.1:latest",
  "pdf_text": ""
}
```

Field explanation:

* `message`: The user’s chat message.
* `model`: The AI model selected for response generation.
* `pdf_text`: Text extracted from an uploaded PDF. This is currently passed as an empty string if no PDF text is provided.

Example response:

```json
{
  "response": "AI-generated response here"
}
```

### Key Frontend Functions

The frontend uses JavaScript to handle chat interaction.

* `addMessage(message, type)`: Adds a new message bubble to the chat history.
* `sendBtn.addEventListener("click", ...)`: Detects when the user clicks the Send button.
* `fetch(`${BACKEND_URL}/chat`, ...)`: Sends the user message to the backend using JSON.
* `userInput.addEventListener("keydown", ...)`: Allows the Enter key to send a message.

## Data / Assumptions

The system exchanges data using JSON between the frontend and backend.

The frontend sends:

```json
{
  "message": "user input",
  "model": "llama3.1:latest",
  "pdf_text": ""
}
```

The backend returns:

```json
{
  "response": "AI response"
}
```

Assumptions made:

* The backend server is running before the frontend sends requests.
* The frontend receives the backend URL from the `.env` file.
* Ollama must be running locally if a local model such as `llama3.1:latest` is used.
* Gemini requires a valid `GOOGLE_API_KEY`.
* PDF upload is included in the interface, but full PDF parsing may require further enhancement depending on the final implementation.
* The chatbot response depends on the selected AI model, so output may vary between Gemini and Llama.

## Testing

### Frontend Testing

The frontend was tested by opening:

```text
http://127.0.0.1:8000
```

Test cases:

* Confirmed that the chat page loads correctly.
* Confirmed that the user can type a message.
* Confirmed that clicking the Send button adds the user message to the chat history.
* Confirmed that pressing Enter also sends the message.
* Confirmed that `BACKEND_URL` is loaded from the frontend `.env` file.
* Confirmed that the frontend receives and displays backend responses.

### Backend Testing

The backend was tested using FastAPI Swagger UI:

```text
http://127.0.0.1:8001/docs
```

Test payload:

```json
{
  "message": "Tell me one Malaysian joke",
  "model": "llama3.1:latest",
  "pdf_text": ""
}
```

The backend returned a successful `200 OK` response with an AI-generated reply.

### Integration Testing

The frontend and backend were tested together by running both services locally:

* Frontend on port `8000`
* Backend on port `8001`

The browser sends a request from the frontend to the backend. CORS middleware is used in the backend to allow requests from the frontend origin.

## Limitations

The current system has several limitations:

* Chat history is only stored on the webpage temporarily. It is not saved to a database.
* There is no user login or authentication.
* AI responses may not always be fully accurate because they depend on the selected model.
* If Ollama is not running, local models such as Llama will not respond.
* Gemini may fail if the API key is missing, invalid, or rate-limited.
* PDF upload is available in the interface, but full PDF text extraction may require further implementation.
* The frontend interface is simple and does not include advanced styling or conversation management.
* Long user messages or large PDF text may affect response speed.

## Architecture Reflection

The system uses a frontend/backend separation to follow a simple microservices-style architecture. The frontend focuses on the user interface, while the backend handles AI processing and model communication. This makes the system easier to maintain because UI changes can be made without changing the AI logic, and backend logic can be improved without redesigning the webpage.

Environment variables were used to avoid hardcoding configuration values such as the backend URL and API keys. This makes the project more flexible when moving from local development to Docker or another deployment environment.

The main trade-off is that this design is slightly more complex than putting everything into one Python file. Two services must be started during local development, and CORS must be configured because the frontend and backend run on different ports. However, this structure is closer to a real-world application and prepares the project for Docker Compose.

If given more time, I would improve the system by adding full PDF text extraction, storing chat history in a database, adding a model selection dropdown, improving the frontend interface, and deploying the application to a cloud platform.
