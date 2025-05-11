from sqlmodel import Field, Relationship, SQLModel
from typing import Optional

class Country(SQLModel, table=True, metadata={"table_name": "country"}):
    """
    Modelo de país para la base de datos.
    """
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    name: str = Field(max_length=100, unique=True, index=True)

    employee: "Employee" = Relationship(back_populates="country")
    