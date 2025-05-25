from sqlmodel import Field, Relationship, SQLModel
from typing import Optional


class State(SQLModel, table=True):
    """
    Modelo de estado o provincia para la base de datos.
    """

    __tablename__ = "state"  # type: ignore
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    name: str = Field(max_length=100, index=True)
    country_id: int = Field(foreign_key="country.id")

    employee: "Employee" = Relationship(back_populates="state")
