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
    date: date
    register_type: RegisterType
    first_check_in: time
    last_check_out: time
    check_count: int
    amount: float
    hours: time
    pay: bool
    notes: str

    employee: "Employee" = Relationship(back_populates="employee_hours")
    concept: "Concept" = Relationship(back_populates="employee_hours")
    shift: "Shift" = Relationship(back_populates="employee_hours")
