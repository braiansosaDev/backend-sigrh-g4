from typing import Optional, Any
from pydantic import BaseModel, Field, field_validator
from enum import Enum, StrEnum
from datetime import date, datetime
from src.modules.ability.schemas.ability_schemas import AbilityPublic
from src.modules.postulation.models.postulation_models import Postulation
from src.modules.postulation.schemas.postulation_schemas import PostulationResponse


class JobOpportunityAbilityImportance(StrEnum):
    REQUERIDA = "requerida"
    DESEADA = "deseada"


class JobOpportunityStatus(StrEnum):
    ACTIVO = "activo"
    NO_ACTIVO = "no_activo"


class JobOpportunityWorkMode(StrEnum):
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
    required_skill_percentage: float = Field(ge=0.0, le=100.0)
    desirable_skill_percentage: float = Field(ge=0.0, le=100.0)


class JobOpportunityRequest(BaseModel):
    owner_employee_id: Optional[int] = Field()
    status: JobOpportunityStatus = Field()
    work_mode: JobOpportunityWorkMode = Field()
    title: str = Field(min_length=1, max_length=100)
    description: str = Field(min_length=1, max_length=1000)
    budget: int = Field(gt=0)
    budget_currency_id: str = Field(min_length=3, max_length=3)
    state_id: int = Field()
    required_abilities: list[AbilityPublic] = Field()
    desirable_abilities: list[AbilityPublic] = Field()
    required_skill_percentage: float = Field(ge=0.0, le=100.0)
    desirable_skill_percentage: float = Field(ge=0.0, le=100.0)

    @field_validator("title", mode="before")
    def title_validator(cls, title: Any):
        if type(title) is not str:
            raise ValueError("El título no es una string.")
        if not title.strip():
            raise ValueError("El título no puede estar vacío.")
        elif len(title) > 100:
            raise ValueError("El título no puede tener más de 100 caracteres.")
        return title

    @field_validator("description", mode="before")
    def description_validator(cls, description: Any):
        if type(description) is not str:
            raise ValueError("La descripción no es una string.")
        if not description.strip():
            raise ValueError("La descripción no puede estar vacía.")
        elif len(description) > 1000:
            raise ValueError("La descripción no puede tener más de 1000 caracteres.")
        return description


class JobOpportunityResponse(JobOpportunityRequest):
    id: int = Field()
    created_at: datetime = Field()
    updated_at: datetime = Field()

class JobOpportunityAndPostulationsResponse(JobOpportunityResponse):
    postulations: Optional[list[Postulation]] = None

class JobOpportunityActiveCountRequest(BaseModel):
    from_date: datetime = Field(
        description="Fecha de inicio del rango de búsqueda."
    )
    to_date: datetime = Field(
        description="Fecha de fin del rango de búsqueda."
    )

    @field_validator("from_date","to_date", mode="before")
    def from_date_validator(cls, date: Any):
        if isinstance(date, datetime) and date > datetime.now():
            raise ValueError("La fecha de inicio o fin no puede ser futura.")
        return date


class JobOpportunityActiveCountResponse(BaseModel):
    active_count: int = Field()
    inactive_count: int = Field()
    
    
class JobOpportunityPublic(BaseModel):
    id: int = Field()
    owner_employee_id: int = Field()
    status: JobOpportunityStatus = Field()
    work_mode: JobOpportunityWorkMode = Field()
    title: str = Field(min_length=1, max_length=100)
    description: str = Field(min_length=1, max_length=1000)


class GetRequest(BaseModel):
    model_config = {"extra": "forbid"}
    
    oportunity_status: Optional[list[JobOpportunityStatus]] = None
    owner_employee_id: Optional[list[int]] = None
    from_creation_date: Optional[date] = None
    until_creation_date: Optional[date] = None
