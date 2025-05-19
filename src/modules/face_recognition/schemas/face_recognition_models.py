from typing import Optional
from pydantic import BaseModel


class FaceRecognitionBaseModel(BaseModel):
    """
    Modelo base para el registro facial.
    """
    id: int | None
    employee_id: int 
    # image_base64: str | None = Field(max_length=1000)

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
    embedding: Optional[list[float]] 

class VerifyFaceRegistration(BaseModel):
    """
    Modelo para verificar un registro facial.
    """
    embedding: Optional[list[float]] 

