from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from sqlalchemy.sql import func
from src.modules.opportunity.schemas.job_opportunity_schemas import (
    JobOpportunityStatus,
    JobOpportunityWorkMode,
    JobOpportunityAbilityImportance,
)
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.modules.employees.models.employee import Employee


class JobOpportunityBaseModel(SQLModel):
    """
    Contiene todos los atributos comunes a todos
    los modelos de JobOpportunity.
    """

    owner_employee_id: int = Field(foreign_key="employee.id", ondelete="CASCADE")
    status: JobOpportunityStatus = Field()
    work_mode: JobOpportunityWorkMode = Field()
    title: str = Field(min_length=1, max_length=100)
    description: str = Field(min_length=1, max_length=1000)
    budget: int = Field(gt=0)
    budget_currency_id: str = Field(min_length=3, max_length=3)
    state_id: int = Field()
    created_at: datetime = Field(default=func.now())
    updated_at: datetime = Field(
        default=func.now(), sa_column_kwargs={"onupdate": func.now()}
    )


class JobOpportunityModel(JobOpportunityBaseModel, table=True):
    """
    Modelo de JobOpportunity que representa la tabla de la base
    de datos. El `id` puede ser `None` porque este model se
    utiliza para cargar los datos, luego se envía a la database
    y esta crea el `id` correspondiente.
    """

    __tablename__ = "job_opportunity"  # type: ignore

    id: int | None = Field(primary_key=True, index=True)
    employee: "Employee" = Relationship(back_populates="job_opportunity")


class JobOpportunityIdModel(JobOpportunityBaseModel):
    """
    Modelo que representa una tabla de la base de datos
    que obligatoriamente tiene una ID. Se utiliza para
    eliminar warnings de `id` con posible valor `None`
    cuando realmente sabemos que existe porque obtuvimos
    el objeto de la base de datos.
    """

    id: int = Field(primary_key=True, index=True)


class JobOpportunityAbility(SQLModel, table=True):
    __tablename__ = "job_opportunity_ability"  # type: ignore

    job_opportunity_id: int = Field(primary_key=True, foreign_key="job_opportunity.id")
    ability_id: int = Field(primary_key=True, foreign_key="ability.id")
    ability_type: JobOpportunityAbilityImportance = Field()
