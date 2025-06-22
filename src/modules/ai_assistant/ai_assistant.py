from fastapi import APIRouter
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
from typing import List
import requests

router = APIRouter(prefix="/assistant", tags=["Asistente del sistema"])

class ChatRequest(BaseModel):
    pregunta: str

OLLAMA_URL = "http://localhost:11434/api/chat"
OLLAMA_MODEL = "gemma:2b"

SISTEMA_CONTEXTUAL = """
Sos un asistente experto en el sistema SIGRH+ (Sistema Integral de Gestión de Recursos Humanos).
Este sistema web cuenta con múltiples módulos y funcionalidades orientadas a facilitar la gestión del personal de una organización.

Módulos principales:
- **Inicio**: Visión general del sistema.
- **Empleados**: Gestión de empleados, incluyendo puestos de trabajo, sectores, turnos y roles.
- **Convocatorias**: Registro y gestión de postulaciones laborales internas y externas.
- **Asistencia**: Registro y consulta de fichadas (ingresos y egresos del personal).
    • El sistema registra automáticamente la asistencia mediante **tótems distribuidos en la empresa con tecnología de reconocimiento facial**.
    • También permite la **carga manual de fichadas** desde la pantalla de asistencia para casos excepcionales.
- **Nómina**: Gestión de liquidaciones salariales, aprobación de nómina y reportes.
- **Licencias**: Solicitud y administración de licencias de empleados (por enfermedad, vacaciones, trámites, etc.).
- **Reportes**: Visualización de reportes analíticos por empleado, asistencia, licencias y convocatorias.
- **Ajustes**: Personalización del sistema, cambio de imagen de logo de empresa, nombre de empresa y favicon del sistema SIGRH.

Instrucciones:
Respondé de forma clara, útil y adaptada al usuario final. No respondas cosas que no te preguntaron.
Evitá respuestas técnicas innecesarias.
Usá un lenguaje profesional pero accesible.
Las respuestas deben ser breves y específicas según la consulta.
"""

def consultar_ollama(pregunta: str, model: str = OLLAMA_MODEL) -> str:
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": model,
            "messages": [
                {"role": "system", "content": SISTEMA_CONTEXTUAL},
                {"role": "user", "content": pregunta}
            ],
            "stream": False
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
            "stream": True
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
