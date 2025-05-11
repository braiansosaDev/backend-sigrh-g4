from sqlmodel import Field, Relationship, SQLModel
from typing import Optional, List

class Sector(SQLModel, table=True, metadata={"table_name": "sector"}):
    """
    Modelo de Sector para la base de datos.
    """
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    name: str = Field(max_length=100, unique=True, index=True)

    # Relación inversa (sector tiene muchos jobs)
    job: List["Job"] = Relationship(back_populates="sector")
    