from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
import os

load_dotenv()

BACKEND_URL = os.getenv("BACKEND_URL")

app = FastAPI()

templates = Jinja2Templates(directory="src/templates")


# Day 1 proof
@app.get("/hello")
def hello(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="hello_world.html",
    )


# Day 2 chat page
@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="chat_page.html",
        context={
            "backend_url": BACKEND_URL
        }
    )
