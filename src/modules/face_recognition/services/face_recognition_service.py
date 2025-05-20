from fastapi import HTTPException, status
from sqlmodel import select
from src.database.core import DatabaseSession
from src.modules.employees.models.employee import Employee
from src.modules.face_recognition.models.face_recognition import FaceRecognition
from src.modules.face_recognition.schemas.face_recognition_models import (
    CreateFaceRegistration,
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

    # Crear el nuevo registro
    employee_id = create_face_register_request.employee_id
    db_face_register = FaceRecognition(
        employee_id=employee_id,
        embedding=new_embedding,
    )
    db.add(db_face_register)
    db.commit()
    db.refresh(db_face_register)

    employee = db.exec(
        select(Employee).where(Employee.id == employee_id)
    ).one_or_none()

    if employee is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found."
        )

    employee.face_recognition_id = db_face_register.id
    db.add(employee)
    db.commit()
    db.refresh(employee)

    return db_face_register


def verify_face(
    db: DatabaseSession, verify_face_recognition_request: VerifyFaceRegistration
) -> bool:
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
                print(f"Verified: employee_id {face.employee_id}")
                print(f"Verified: id de face {face.id}")
                return True

    print("Not verified: no match found")
    return False


def update_face_register(
    db: DatabaseSession, employee_id: int, update_face_register_request: UpdateFaceRegistration
) -> FaceRecognitionBaseModel:
    db_face_register = db.exec(
        select(FaceRecognition).where(FaceRecognition.employee_id == employee_id)
    ).one_or_none()

    if db_face_register is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Face not found."
        )

    db_face_register.embedding = update_face_register_request.embedding
    db.add(db_face_register)
    db.commit()
    db.refresh(db_face_register)
    return db_face_register


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
