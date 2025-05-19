from fastapi import APIRouter

from src.database.core import DatabaseSession

from fastapi import status
import logging

from src.modules.face_recognition.schemas.face_recognition_models import CreateFaceRegistration, FaceRecognitionBaseModel, VerifyFaceRegistration
from src.modules.face_recognition.services import face_recognition_service


logger = logging.getLogger("uvicorn.error")
face_recognition_router = APIRouter(prefix="/face_recognition", tags=["face_recognition"])


@face_recognition_router.post("/register", response_model=FaceRecognitionBaseModel, status_code=status.HTTP_201_CREATED)
async def register_face(
    db: DatabaseSession,
    face_recognition: CreateFaceRegistration,
) -> FaceRecognitionBaseModel:
    return face_recognition_service.create_face_register(db, face_recognition)


@face_recognition_router.post("/", response_model=FaceRecognitionBaseModel, status_code=status.HTTP_202_ACCEPTED)
async def verify_face(
    db: DatabaseSession,
    face_recognition: VerifyFaceRegistration,
) -> FaceRecognitionBaseModel:
    """
    Verifica el rostro de un empleado.
    """
    logger.info("Verificando rostro...")
    return face_recognition_service.verify_face(db, face_recognition)

