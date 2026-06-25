from fastapi import FastAPI
from pydantic import BaseModel

from week2.prompt_model import prompt_model
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str
    model: str = "llama3.1:latest"
    pdf_text: str = ""


@app.post("/chat")
def chat(request: ChatRequest):
    full_prompt = f"""
User message:
{request.message}

PDF text:
{request.pdf_text}
"""

    response = prompt_model(request.model, full_prompt)

    return {
        "response": response
    }