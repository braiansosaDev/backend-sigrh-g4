from enum import Enum
from typing import Any
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime


class PostulationStatus(Enum):
    PENDIENTE = "pendiente"
    ACEPTADA = "aceptada"
    NO_ACEPTADA = "no aceptada"
    CONTRATADO = "contratado"
    RECHAZADO = "rechazado"


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


class RejectedOptions(Enum):
    NO_CUMPLE_CON_LOS_REQUISITOS_DEL_PUESTO = "No cumple con los requisitos del puesto"
    FALTA_DE_EXPERIENCIA_RELEVANTE = "Falta de experiencia relevante"
    NO_POSEE_LA_FORMACION_ACADEMICA_REQUERIDA = "No posee la formación académica requerida"
    NO_SE_AJUSTA_AL_PERFIL_BUSCADO = "No se ajusta al perfil buscado"
    NO_DISPONIBILIDAD_HORARIA = "No disponibilidad horaria"
    NO_PASO_LA_ENTREVISTA_TECNICA = "No pasó la entrevista técnica"
    NO_PASO_LA_ENTREVISTA_DE_RRHH = "No pasó la entrevista de RRHH"
    PROCESO_CERRADO_POR_COBERTURA_INTERNA = "Proceso cerrado por cobertura interna"
    POSTULANTE_SOLICITABA_SALARIO_ALTO = "Postulante solicitaba salario alto"
    POSTULANTE_NO_INTERESADO_EN_LA_PROPUESTA = "Postulante no interesado en la propuesta"
    POSTULANTE_NO_SE_PRESENTO_A_LA_ENTREVISTA = "Postulante no se presentó a la entrevista"
    POSTULANTE_RETIRO_SU_POSTULACION = "Postulante retiró su postulación"
    POSTULANTE_ACEPTO_OTRA_OFERTA = "Postulante aceptó otra oferta"
    OTRO_MOTIVO = "Otro motivo"
    NO_ESPECIFICADO = "No especificado"

class RejectedPostulationsResponse(BaseModel):
    opportunity_id: int
    motivos: dict[str, int]