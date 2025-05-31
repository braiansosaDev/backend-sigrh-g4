from fastapi import APIRouter

from src.database.core import DatabaseSession

from fastapi import status
import logging

from src.modules.clock_events.schemas.schemas import ClockEventTypes
from src.modules.face_recognition.schemas.face_recognition_models import (
    CreateFaceRegistration,
    FaceRecognitionBaseModel,
    UpdateFaceRegistration,
    VerifyFaceRegistration,
    OperationStatus,
)
from src.modules.face_recognition.services import face_recognition_service


logger = logging.getLogger("uvicorn.error")
face_recognition_router = APIRouter(
    prefix="/face_recognition", tags=["Face Recognition"]
)


@face_recognition_router.post(
    "/register",
    response_model=FaceRecognitionBaseModel,
    status_code=status.HTTP_201_CREATED,
)
async def register_face(
    db: DatabaseSession,
    face_recognition: CreateFaceRegistration,
) -> FaceRecognitionBaseModel:
    """
    Registra el rostro de un empleado.
    """
    return face_recognition_service.create_face_register(db, face_recognition)


@face_recognition_router.post(
    "/", response_model=OperationStatus, status_code=status.HTTP_200_OK
)
async def verify_face(
    db: DatabaseSession,
    face_recognition: VerifyFaceRegistration,
) -> OperationStatus:
    """
    Verifica el rostro de un empleado.
    """
    logger.info("Verificando rostro...")
    return face_recognition_service.verify_face(db, face_recognition)


@face_recognition_router.patch(
    "/update", response_model=FaceRecognitionBaseModel, status_code=status.HTTP_200_OK
)
async def update_face(
    db: DatabaseSession,
    face_recognition: UpdateFaceRegistration,
) -> FaceRecognitionBaseModel:
    """
    Actualiza el rostro de un empleado.
    """
    logger.info("Actualizando rostro...")
    return face_recognition_service.update_face_register(db, face_recognition)


@face_recognition_router.post(
    "/{event_type}",
    response_model=OperationStatus,
    status_code=status.HTTP_202_ACCEPTED,
)
async def register_attendance(
    event_type: ClockEventTypes,
    db: DatabaseSession,
    face_recognition: VerifyFaceRegistration,
) -> OperationStatus:
    """
    Verifica el rostro de un empleado y lo registra como presente o egreso, según el tipo.
    """
    logger.info(f"Registrando {event_type}...")

    # Asignar device según el tipo
    match event_type:
        case ClockEventTypes.IN:
            device_id = "Totem de reconocimiento facial ingreso."
        case ClockEventTypes.OUT:
            device_id = "Totem de reconocimiento facial egreso."

    return face_recognition_service.register_attendance(
        db, face_recognition, event_type=event_type, device_id=device_id
    )
