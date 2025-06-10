from enum import Enum
from typing import Any
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime


class PostulationStatus(Enum):
    PENDIENTE = "pendiente"
    ACEPTADA = "aceptada"
    NO_ACEPTADA = "no aceptada"
    CONTRATADO = "contratado"


class PostulationCreate(BaseModel):
    """
    Schema de postulación utilizado para
    crear postulaciones.
    """

    job_opportunity_id: int = Field()
    name: str = Field(min_length=1, max_length=50)
    surname: str = Field(min_length=1, max_length=50)
    email: EmailStr = Field(min_length=1, max_length=100)
    phone_number: str = Field(min_length=1, max_length=100)
    address_country_id: int = Field()
    address_state_id: int = Field()
    cv_file: str = Field()


class PostulationResponse(PostulationCreate):
    """
    Schema de postulación utilizado para
    devolver la información de una postulación
    """

    id: int = Field()
    evaluated_at: datetime | None = Field(default=None)
    suitable: bool = Field(default=False)
    ability_match: dict[str, Any] = Field()
    created_at: datetime = Field()
    updated_at: datetime = Field()
    status: PostulationStatus = Field()
    motive: str | None


class PostulationUpdate(BaseModel):
    """
    Schema de postulación utilizado para
    actualizar postulaciones
    """

    job_opportunity_id: int | None = Field(default=None)
    name: str | None = Field(min_length=1, max_length=50, default=None)
    surname: str | None = Field(min_length=1, max_length=50, default=None)
    email: EmailStr | None = Field(min_length=1, max_length=100, default=None)
    phone_number: str | None = Field(min_length=1, max_length=100, default=None)
    address_country_id: int | None = Field(default=None)
    address_state_id: int | None = Field(default=None)
    cv_file: str | None = Field(default=None)
    status: PostulationStatus = Field()
    motive: str | None
