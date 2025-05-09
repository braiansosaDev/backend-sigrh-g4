from pydantic import BaseModel, Field, field_validator
from enum import Enum
from datetime import datetime
from src.modules.ability.schemas.ability_schemas import AbilityPublic
from pydantic import EmailStr

class JobOpportunityAbilityImportance(Enum):
    REQUERIDA = "requerida"
    DESEADA = "deseada"

class JobOpportunityStatus(Enum):
    ACTIVO = "activo"
    NO_ACTIVO = "no_activo"


class JobOpportunityWorkMode(Enum):
    REMOTO = "remoto"
    HIBRIDO = "hibrido"
    PRESENCIAL = "presencial"


class JobOpportunityUpdate(BaseModel):
     owner_employee_id: int | None = Field(default=None)
     status: JobOpportunityStatus | None = Field(default=None)
     work_mode: JobOpportunityWorkMode | None = Field(default=None)
     title: str | None = Field(min_length=1, max_length=100, default=None)
     description: str | None = Field(min_length=1, max_length=1000, default=None)
     budget: int | None = Field(gt=0, default=None)
     budget_currency_id: str | None = Field(min_length=3, max_length=3, default=None)
     state_id: int | None = Field(default=None)
     required_abilities: list[AbilityPublic] | None = Field(default=None)
     desirable_abilities: list[AbilityPublic] | None = Field(default=None)


class JobOpportunityRequest(BaseModel):
    owner_employee_id: int = Field()
    status: JobOpportunityStatus = Field()
    work_mode: JobOpportunityWorkMode = Field()
    title: str = Field(min_length=1, max_length=100)
    description: str = Field(min_length=1, max_length=1000)
    budget: int = Field(gt=0)
    budget_currency_id: str = Field(min_length=3, max_length=3)
    state_id: int = Field()
    required_abilities: list[AbilityPublic] = Field()
    desirable_abilities: list[AbilityPublic] = Field()

    @field_validator("title", mode="before")
    def title_validator(cls, title):
        if type(title) is not str:
            raise TypeError("El título no es una string.")
        if not title.strip():
            raise ValueError("El título no puede estar vacío.")
        elif len(title) > 100:
            raise ValueError("El título no puede tener más de 100 caracteres.")
        return title

    @field_validator("description", mode="before")
    def description_validator(cls, description):
        if type(description) is not str:
            raise TypeError("La descripción no es una string.")
        if not description.strip():
            raise ValueError("La descripción no puede estar vacía.")
        elif len(description) > 1000:
            raise ValueError("La descripción no puede tener más de 1000 caracteres.")
        return description

class JobOpportunityResponse(JobOpportunityRequest):
    id: int = Field()
    created_at: datetime = Field()
    updated_at: datetime = Field()


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
    cv_file: bytes = Field()


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
    cv_file: bytes | None = Field(default=None)
