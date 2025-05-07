from sqlmodel import SQLModel, Field
from enum import Enum
from datetime import datetime
from src.modules.ability.schemas.ability_schemas import AbilityPublic


class JobOpportunityStatus(Enum):
    ACTIVO = "activo"
    NO_ACTIVO = "no_activo"


class JobOpportunityWorkMode(Enum):
    REMOTO = "remoto"
    HIBRIDO = "hibrido"
    PRESENCIAL = "presencial"


class JobOpportunityBase(SQLModel):
    owner_employee_id: int = Field(foreign_key="employee.id")
    status: JobOpportunityStatus = Field()
    work_mode: JobOpportunityWorkMode = Field()
    title: str = Field(max_length=100)
    description: str = Field(max_length=500)
    budget: int = Field(gt=0)
    budget_currency_id: str = Field(max_length=3)
    state_id: int = Field(foreign_key="state.id")
    created_at: datetime = Field()
    updated_at: datetime = Field()


class JobOpportunityBaseId(JobOpportunityBase):
    id: int = Field(primary_key=True, index=True)


class JobOpportunityRequest(JobOpportunityBase):
    job_opportunity_abilities: list[AbilityPublic] = Field()


class JobOpportunityResponse(JobOpportunityRequest):
    id: int = Field(primary_key=True, index=True)
