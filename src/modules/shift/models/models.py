from sqlmodel import Field, SQLModel, Relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.modules.employees.models.employee import Employee, EmployeeHours


class Shift(SQLModel, table=True):
    __tablename__ = "shift"  # type: ignore
    id: int = Field(primary_key=True)
    description: str
    type: str  # Matutino, Nocturno, Vespertino
    working_hours: float
    working_days: int

    employee: "Employee" = Relationship(back_populates="shift")
    employee_hours: list["EmployeeHours"] = Relationship(back_populates="shift")
