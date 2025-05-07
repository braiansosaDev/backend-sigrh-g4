from sqlmodel import SQLModel, Field
from datetime import datetime
from pydantic import EmailStr
from sqlalchemy import JSON, Column
from src.modules.opportunity.schemas.job_opportunity_schemas import JobOpportunityBase


class JobOpportunity(JobOpportunityBase, table=True):
    """
    Modelo de JobOpportunity para la base de datos
    """

    __tablename__ = "job_opportunity"  # type: ignore

    id: int | None = Field(primary_key=True, index=True)


class JobOpportunityAbility(SQLModel, table=True):
    __tablename__ = "job_opportunity_ability"  # type: ignore

    id: int | None = Field(primary_key=True)
    job_opportunity_id: int = Field(foreign_key="job_opportunity.id")
    ability_id: int = Field(foreign_key="ability.id")


# TODO: Eliminar cuando se haga el merge
class Country(SQLModel, table=True):
    __tablename__ = "country"  # type: ignore

    id: int | None = Field(primary_key=True, index=True)
    name: str = Field(max_length=100)


# TODO: Eliminar cuando se haga el merge
class State(SQLModel, table=True):
    __tablename__ = "state"  # type: ignore

    id: int | None = Field(primary_key=True, index=True)
    name: str = Field(max_length=100)
    country_id: int = Field(foreign_key="country.id")


class Postulation(SQLModel, table=True):
    """
    Modelo de postulación para la base de datos, que representa los datos que
    ingresó el postulante.
    """

    __tablename__: str = "postulation"  # type: ignore

    id: int = Field(primary_key=True, index=True)
    job_opportunity_id: int = Field(foreign_key="job_opportunity.id")
    name: str = Field(max_length=50)
    surname: str = Field(max_length=50)
    email: EmailStr = Field(max_length=100)
    phone_number: int = Field(max_length=100)
    address_country_id: int = Field(foreign_key="country.id")
    address_state_id: int = Field(foreign_key="state.id")
    cv_file: bytes = Field()
    evaluated_at: datetime = Field()
    suitable: bool = Field()
    ability_match: dict = Field(sa_column=Column(JSON), default_factory=dict)
    created_at: datetime = Field()
