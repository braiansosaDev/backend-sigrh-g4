from sqlmodel import Field, Relationship, SQLModel
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from src.modules.employees.models.employee import Employee
    from src.modules.employees.models.sector import Sector

class Job(SQLModel, table=True, metadata={"table_name": "job"}):
    """
    Modelo de puesto o job para la base de datos.
    """
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    name: str = Field(max_length=100, index=True)
    sector_id: int = Field(foreign_key="sector.id")

    employee: "Employee" = Relationship(back_populates="job")
    sector: Optional["Sector"] = Relationship(back_populates="job")
