from fastapi import APIRouter

from src.database.core import DatabaseSession

from fastapi import status
import logging

from src.modules.face_recognition.schemas.face_recognition_models import CreateFaceRegistration, FaceRecognitionBaseModel, UpdateFaceRegistration, VerifyFaceRegistration, OperationStatus
from src.modules.face_recognition.services import face_recognition_service


logger = logging.getLogger("uvicorn.error")
face_recognition_router = APIRouter(prefix="/face_recognition", tags=["face_recognition"])


@face_recognition_router.post("/register", response_model=FaceRecognitionBaseModel, status_code=status.HTTP_201_CREATED)
async def register_face(
    db: DatabaseSession,
    face_recognition: CreateFaceRegistration,
) -> FaceRecognitionBaseModel:
    """
    Registra el rostro de un empleado.
    """
    return face_recognition_service.create_face_register(db, face_recognition)


@face_recognition_router.get("/", response_model=FaceRecognitionBaseModel, status_code=status.HTTP_200_OK)
async def verify_face(
    db: DatabaseSession,
    face_recognition: VerifyFaceRegistration,
) -> OperationStatus:
    """
    Verifica el rostro de un empleado.
    """
    logger.info("Verificando rostro...")
    return face_recognition_service.verify_face(db, face_recognition)


@face_recognition_router.patch("/update", response_model=FaceRecognitionBaseModel, status_code=status.HTTP_200_OK)
async def update_face(
    db: DatabaseSession,
    face_recognition: UpdateFaceRegistration,
) -> FaceRecognitionBaseModel:
    """
    Actualiza el rostro de un empleado.
    """
    logger.info("Actualizando rostro...")
    return face_recognition_service.update_face_register(db, face_recognition)


@face_recognition_router.post("/in", response_model=FaceRecognitionBaseModel, status_code=status.HTTP_202_OK)
async def check_in(
    db: DatabaseSession,
    face_recognition: VerifyFaceRegistration,
) -> OperationStatus:
    """
    Verifica el rostro de un empleado y lo registra como presente.
    """
    logger.info("Registrando entrada...")
    return face_recognition_service.check_in(db, face_recognition)

@face_recognition_router.post("/out", response_model=FaceRecognitionBaseModel, status_code=status.HTTP_202_OK)
async def check_out(
    db: DatabaseSession,
    face_recognition: VerifyFaceRegistration,
) -> OperationStatus:
    """
    Verifica el rostro de un empleado y lo registra como egreso.
    """
    logger.info("Registrando salida...")
    return face_recognition_service.check_out(db, face_recognition)