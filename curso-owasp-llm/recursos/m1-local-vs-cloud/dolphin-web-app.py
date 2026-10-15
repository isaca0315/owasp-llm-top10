from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import requests

app = FastAPI()

class Message(BaseModel):
    message: str

@app.post("/chat")
def chat(msg: Message):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "dolphin-llama3:latest",
                "prompt": msg.message,
                "stream": False
            }
        )

        data = response.json()

        if "response" in data:
            return {"response": data["response"]}
        else:
            return {"response": f"Ollama error: {data}"}

    except Exception as e:
        return {"response": f"Server error: {str(e)}"}



app.mount("/", StaticFiles(directory="static", html=True), name="static")
