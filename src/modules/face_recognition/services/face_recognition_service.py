from datetime import datetime
from fastapi import HTTPException, status
from sqlmodel import select
from src.database.core import DatabaseSession
from src.modules.clock_events.schemas.schemas import ClockEventRequest
from src.modules.clock_events.services.services import post_clock_event
from src.modules.employees.models.employee import Employee
from src.modules.face_recognition.models.face_recognition import FaceRecognition
from src.modules.face_recognition.schemas.face_recognition_models import (
    CreateFaceRegistration,
    OperationStatus,
    UpdateFaceRegistration,
    VerifyFaceRegistration,
    FaceRecognitionBaseModel,
)
import numpy as np
from typing import List


THRESHOLD = 0.6  # distancia máxima aceptada para considerar una coincidencia


def euclidean_distance(vec1: List[float], vec2: List[float]) -> float:
    return np.linalg.norm(np.array(vec1) - np.array(vec2))


def get_all_faces(db: DatabaseSession):
    return db.exec(select(FaceRecognition)).all()


def create_face_register(
    db: DatabaseSession, create_face_register_request: CreateFaceRegistration
) -> FaceRecognitionBaseModel:
    # Verificar si ya existe un rostro similar
    new_embedding = create_face_register_request.embedding
    db_faces = get_all_faces(db)

    for face in db_faces:
        if face.embedding:
            distance = euclidean_distance(face.embedding, new_embedding)
            if distance < THRESHOLD:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="A similar face already exists in the system.",
                )

    # Crear el nuevo registro\
    employee_id = create_face_register_request.employee_id
    db_face_register = FaceRecognition(
        employee_id=employee_id,
        embedding=new_embedding,
    )
    db.add(db_face_register)
    db.commit()
    db.refresh(db_face_register)

    return db_face_register


def verify_face(
    db: DatabaseSession, verify_face_recognition_request: VerifyFaceRegistration
) -> OperationStatus:
    db_faces = get_all_faces(db)

    if not db_faces:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No registered faces to compare with."
        )

    input_embedding = verify_face_recognition_request.embedding

    for face in db_faces:
        if face.embedding:
            distance = euclidean_distance(face.embedding, input_embedding)
            if distance < THRESHOLD:
                return OperationStatus(
                    success=True,
                    message=f"Face verified successfully. Employee ID: {face.employee_id}",
                    employee_id=face.employee_id,
                )

    return OperationStatus(employee_id=None, success=False, message="No match found.")



def update_face_register(
    db: DatabaseSession, update_face_register_request: UpdateFaceRegistration
) -> FaceRecognitionBaseModel:
    db_face_register = db.exec(
        select(FaceRecognition).where(FaceRecognition.employee_id == update_face_register_request.employee_id)
    ).one_or_none()

    if db_face_register is None:
        result = create_face_register(db, update_face_register_request)
        # raise HTTPException(
        #     status_code=status.HTTP_404_NOT_FOUND, detail="Face not found in database."
        # )
        return result
    else:
        db_face_register.embedding = update_face_register_request.embedding
        db.add(db_face_register)
        db.commit()
        db.refresh(db_face_register)
        result = FaceRecognitionBaseModel(
            id=db_face_register.id,
            employee_id=db_face_register.employee_id,
        )
        return result

def delete_face_register(db: DatabaseSession, employee_id: int) -> None:
    db_face_register = db.exec(
        select(FaceRecognition).where(FaceRecognition.employee_id == employee_id)
    ).one_or_none()

    if db_face_register is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Face not found."
        )

    db.delete(db_face_register)
    db.commit()


def register_attendance(
    db: DatabaseSession, verify_face_recognition_request: VerifyFaceRegistration, event_type: str, device_id: str
) -> OperationStatus:
    db_faces = get_all_faces(db)

    if not db_faces:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No registered faces to compare with."
        )

    input_embedding = verify_face_recognition_request.embedding

    for face in db_faces:
        if face.embedding:
            distance = euclidean_distance(face.embedding, input_embedding)
            if distance < THRESHOLD:
                employee = db.exec(
                    select(Employee).where(Employee.id == face.employee_id)
                ).one_or_none()

                if employee is None:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="Employee not found."
                    )

                post_clock_event(db,ClockEventRequest(
                        employee_id= employee.id,
                        event_type= event_type,
                        event_date= datetime.now(),
                        device_id= device_id,
                        source= "face_recognition"
                ))

                return OperationStatus(
                    success=True,
                    message=f"Check-in successful. Employee ID: {employee.id}",
                    employee_id=employee.id,
                )

    return OperationStatus(employee_id=None, success=False, message="No match found.")
