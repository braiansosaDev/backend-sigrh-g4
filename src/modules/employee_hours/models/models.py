from sqlalchemy import Date, Time
from sqlmodel import Field, Relationship, SQLModel
from src.modules.employees.models.employee import Employee


class EmployeeHours(SQLModel, table=True):
    __tablename__ = "employee_hours"  # type: ignore
    id: int = Field(primary_key=True)
    employee_id: int = Field(foreign_key="employee.id")
    concept_id: int  # incluir la relacion
    shift_id: int  # incluir la relacion
    weekday: int
    date: Date
    register_type: str
    first_check_in: Time
    last_check_out: Time
    check_count: int
    amount: float
    hours: Time
    pay: bool
    notes: str
    employee: Employee = Relationship(back_populates="employee_hours")
