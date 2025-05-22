from sqlmodel import Field, Relationship, SQLModel, CheckConstraint
from datetime import time, date
from enum import Enum


class RegisterType(str, Enum):
    AUSENCIA = "AUSENCIA"
    PRESENCIA = "PRESENCIA"
    TIEMPO_INTERMEDIO = "TIEMPO INTERMEDIO"


class EmployeeHours(SQLModel, table=True):
    __tablename__ = "employee_hours"  # type: ignore
    __table_args__ = (
        CheckConstraint("weekday >= 1 AND weekday <= 7", name="chk_weekday_range"),
    )
    id: int = Field(primary_key=True)
    employee_id: int = Field(foreign_key="employee.id", ondelete="CASCADE")
    concept_id: int = Field(foreign_key="concept.id")
    shift_id: int = Field(foreign_key="shift.id")
    weekday: int
    check_count: int = Field(default=0)
    work_date: date = Field(default=date.today)  # antes: date
    register_type: RegisterType = Field(default=None)
    first_check_in: time = Field(default=None)
    last_check_out: time = Field(default=None)
    time_worked: time = Field(default=None)  # antes: hours
    daily_salary: float = Field(default=0.0)  # antes: amount
    pay: bool = Field(default=False)
    notes: str = Field(default="")

    employee: "Employee" = Relationship(back_populates="employee_hours")
    concept: "Concept" = Relationship(back_populates="employee_hours")
    shift: "Shift" = Relationship(back_populates="employee_hours")
