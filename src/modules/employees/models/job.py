from sqlmodel import Field, Relationship, SQLModel
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from src.modules.employees.models.employee import Employee
    from src.modules.employees.models.sector import Sector


class Job(SQLModel, table=True):
    """
    Modelo de puesto o job para la base de datos.
    """

    __tablename__ = "job" # type: ignore

    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    name: str = Field(max_length=100, index=True)
    sector_id: int = Field(foreign_key="sector.id")

    employees: list["Employee"] = Relationship(back_populates="job", sa_relationship_kwargs={"order_by": "Employee.id"})
    sector: Optional["Sector"] = Relationship(back_populates="job")
