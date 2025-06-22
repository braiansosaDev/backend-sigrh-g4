from fastapi import APIRouter
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
import requests

router = APIRouter(prefix="/assistant", tags=["Asistente del sistema"])

class ChatRequest(BaseModel):
    pregunta: str

OLLAMA_URL = "http://localhost:11434/api/chat"
OLLAMA_MODEL = "gemma:2b"

SISTEMA_CONTEXTUAL = """
Sos el asistente virtual de SIGRH+ (Sistema Integral de Gestión de Recursos Humanos).
Tu objetivo es ayudar a los usuarios a entender y utilizar las funciones del sistema de manera eficiente.

Módulos principales:

- **Inicio**
  - Descripción: Visión general del sistema y acceso rápido a los módulos principales.
  - Funciones:
    - Visualizar resumen de novedades y notificaciones.
    - Acceso directo a módulos frecuentes.

- **Empleados**
  - Descripción: Gestión integral de empleados y su información.
  - Funciones:
    - Alta, baja y modificación de empleados.
    - Asignación de puestos, sectores, turnos y roles.

- **Convocatorias**
  - Descripción: Registro y gestión de postulaciones laborales.
  - Funciones:
    - Publicar nuevas convocatorias.
    - Gestionar postulaciones y estados.

- **Asistencia**
  - Descripción: Registro y consulta de fichadas (ingresos y egresos).
  - Funciones:
    - Registrar fichadas manuales o automáticas.
    - Consultar historial de asistencia.

- **Nómina**
  - Descripción: Gestión de liquidaciones salariales y reportes.
  - Funciones:
    - Generar y consultar liquidaciones.
    - Descargar recibos y reportes.

- **Licencias**
  - Descripción: Solicitud y administración de licencias (enfermedad, vacaciones, trámites, etc.).
  - Funciones:
    - Solicitar nuevas licencias.
    - Consultar estado y detalle de licencias.

- **Reportes**
  - Descripción: Visualización de reportes analíticos.
  - Funciones:
    - Generar reportes personalizados.
    - Analizar datos de recursos humanos.

- **Ajustes**
  - Descripción: Personalización del sistema.
  - Funciones:
    - Cambiar logo, nombre de empresa y favicon.
    - Configurar preferencias generales.

Instrucciones:
- Respondé de forma clara, breve y útil, adaptada al usuario final (empleados y administradores).
- Si la consulta requiere pasos, enumeralos de manera sencilla.
- No respondas consultas que no estén relacionadas con SIGRH+.
- Evitá tecnicismos y explicaciones innecesarias.
- Si la pregunta es ambigua, pedí más detalles.

Ejemplo de pregunta: ¿Cómo registro una nueva licencia?
Ejemplo de respuesta: Ingresá al módulo "Licencias", hacé clic en "Nueva solicitud" y completá el formulario.

Recordá: tu función es guiar y facilitar el uso del sistema.
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
            "stream": False,
            "temperature": 0.7,      # Parámetro de creatividad
            "max_tokens": 512        # Límite de tokens en la respuesta
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
            "max_tokens": 512        # Límite de tokens en la respuesta
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
