from sqlmodel import Field, Relationship, SQLModel
from typing import Optional, List, TYPE_CHECKING

if TYPE_CHECKING:
    from src.modules.employees.models.job import Job


class Sector(SQLModel, table=True):
    """
    Modelo de Sector para la base de datos.
    """

    __tablename__ = "sector"  # type: ignore
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    name: str = Field(max_length=100, unique=True, index=True)

    # Relación inversa (sector tiene muchos jobs)
    job: List["Job"] = Relationship(back_populates="sector")
