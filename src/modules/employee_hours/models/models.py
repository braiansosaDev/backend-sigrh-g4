from sqlmodel import Field, Relationship, SQLModel
from datetime import time, date
from enum import Enum


class RegisterType(str, Enum):
    AUSENCIA = "AUSENCIA"
    PRESENCIA = "PRESENCIA"
    TIEMPO_INTERMEDIO = "TIEMPO INTERMEDIO"


class EmployeeHours(SQLModel, table=True):
    __tablename__ = "employee_hours"  # type: ignore

    id: int | None = Field(default=None, primary_key=True)
    employee_id: int | None = Field(
        default=None, foreign_key="employee.id", ondelete="CASCADE"
    )
    concept_id: int | None = Field(default=None, foreign_key="concept.id")
    shift_id: int = Field(foreign_key="shift.id")
    check_count: int = Field(default=0)
    work_date: date = Field(default=date.today)  # antes: date
    register_type: RegisterType = Field(default=None)
    first_check_in: time | None = Field(default=None)
    last_check_out: time | None = Field(default=None)
    sumary_time: time | None = Field(default=None)  # antes: hours
    extra_hours: time | None = Field(default=None)  # antes: amount
    pay: bool = Field(default=False)
    notes: str = Field(default="")

    employee: "Employee" = Relationship(back_populates="employee_hours")
    concept: "Concept" = Relationship(back_populates="employee_hours")
    shift: "Shift" = Relationship(back_populates="employee_hours")
