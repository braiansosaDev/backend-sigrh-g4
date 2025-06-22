from fastapi import APIRouter
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
import requests
from .prompt import prompt

router = APIRouter(prefix="/assistant", tags=["Asistente del sistema"])

class ChatRequest(BaseModel):
    pregunta: str

OLLAMA_URL = "http://localhost:11434/api/chat"
OLLAMA_MODEL = "gemma:2b"

SISTEMA_CONTEXTUAL = prompt

def consultar_ollama(pregunta: str, model: str = OLLAMA_MODEL) -> str:
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": model,
            "messages": [
                {"role": "system", "content": SISTEMA_CONTEXTUAL},
                {"role": "user", "content": pregunta}
            ],
            "stream": False,
            "temperature": 0.7,      # Parámetro de creatividad
        }
    )
    data = response.json()
    return data['message']['content'].strip()

def stream_ollama(pregunta: str, model: str = OLLAMA_MODEL):
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": model,
            "messages": [
                {"role": "system", "content": SISTEMA_CONTEXTUAL},
                {"role": "user", "content": pregunta}
            ],
            "stream": True,
            "temperature": 0.7,      # Parámetro de creatividad
        },
        stream=True
    )

    def generate():
        for line in response.iter_lines():
            if line:
                yield line.decode("utf-8").replace("data: ", "")
    return generate

@router.post("/chat")
def chat(req: ChatRequest):
    try:
        respuesta = consultar_ollama(req.pregunta)
        return {"respuesta": respuesta}
    except Exception as e:
        return {"error": str(e)}

@router.post("/chat-stream")
def chat_stream(req: ChatRequest):
    try:
        stream = stream_ollama(req.pregunta)
        return StreamingResponse(stream(), media_type="text/plain")
    except Exception as e:
        return {"error": str(e)}
