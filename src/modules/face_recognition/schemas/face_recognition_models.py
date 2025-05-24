from typing import Optional
from pydantic import BaseModel


class FaceRecognitionBaseModel(BaseModel):
    """
    Modelo base para el registro facial.
    """
    id: int | None
    employee_id: int 

class CreateFaceRegistration(BaseModel):
    """
    Modelo para crear un registro facial.
    """
    employee_id: int 
    embedding: Optional[list[float]] 


class UpdateFaceRegistration(BaseModel):
    """
    Modelo para actualizar un registro facial.
    """
    employee_id: int
    embedding: Optional[list[float]] 

class VerifyFaceRegistration(BaseModel):
    """
    Modelo para verificar un registro facial.
    """
    embedding: Optional[list[float]] 

class OperationStatus(BaseModel):
    """
    Modelo para el estado de la operación.
    """
    success: bool
    message: str
    employee_id: Optional[int] | None