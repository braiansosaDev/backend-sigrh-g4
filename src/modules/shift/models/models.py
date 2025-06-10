from sqlmodel import Field, SQLModel, Relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.modules.employees.models.employee import Employee, EmployeeHours


class Shift(SQLModel, table=True):
    __tablename__ = "shift"  # type: ignore
    id: int = Field(primary_key=True)
    description: str
    type: str
    working_hours: float
    working_days: int

    employees: list["Employee"] = Relationship(back_populates="shift", sa_relationship_kwargs={"order_by": "Employee.id"})
    employee_hours: list["EmployeeHours"] = Relationship(
        back_populates="shift", sa_relationship_kwargs={"order_by": "EmployeeHours.id"}
    )
