from typing import Any
from sqlmodel import SQLModel, Field, Column, JSON
from sqlalchemy import func
from datetime import datetime
from pydantic import EmailStr
from src.modules.postulation.schemas.postulation_schemas import PostulationStatus


class Postulation(SQLModel, table=True):
    """
    Modelo de postulación para la base de datos, que representa los datos que
    ingresó el postulante.
    """

    __tablename__: str = "postulation"  # type: ignore

    id: int | None = Field(primary_key=True, index=True)
    job_opportunity_id: int = Field(foreign_key="job_opportunity.id")
    name: str = Field(min_length=1, max_length=50)
    surname: str = Field(min_length=1, max_length=50)
    email: EmailStr = Field(min_length=1, max_length=100)
    phone_number: str = Field(min_length=1, max_length=100)
    address_country_id: int = Field(foreign_key="country.id")
    address_state_id: int = Field(foreign_key="state.id")
    cv_file: str = Field()
    evaluated_at: datetime | None = Field(default=None)
    suitable: bool = Field(default=False)
    ability_match: dict[str, Any] = Field(sa_column=Column(JSON), default_factory=dict)
    created_at: datetime = Field(default=func.now())
    updated_at: datetime = Field(
        default=func.now(), sa_column_kwargs={"onupdate": func.now()}
    )
    status: PostulationStatus = Field(default=PostulationStatus.PENDIENTE)
    motive: str = Field(nullable=True)
