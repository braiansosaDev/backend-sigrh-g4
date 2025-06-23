from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
from .prompt import prompt
from src.modules.config.services.config_service import get_str
import requests

router = APIRouter(prefix="/assistant", tags=["Asistente del sistema"])

class ChatRequest(BaseModel):
    pregunta: str
    historial: list[dict] = []

OLLAMA_URL = f"http://{get_str("OLLAMA_HOST")}:{get_str("OLLAMA_PORT")}/api/chat"
OLLAMA_MODEL = get_str("OLLAMA_MODEL")

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
            "temperature": 0.3,      # Parámetro de creatividad
        }
    )
    data = response.json()
    return data['message']['content'].strip()

def stream_ollama(pregunta: str, historial: list[dict], model: str = OLLAMA_MODEL):
    messages = [{"role": "system", "content": SISTEMA_CONTEXTUAL}] + historial + [
        {"role": "user", "content": pregunta}
    ]

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": model,
            "messages": messages,
            "stream": True,
            "temperature": 0.7,
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
        stream = stream_ollama(req.pregunta, req.historial)
        return StreamingResponse(stream(), media_type="text/plain")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
