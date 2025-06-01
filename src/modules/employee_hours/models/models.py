from sqlmodel import Field, Relationship, SQLModel
from datetime import time, date
from enum import Enum
from typing import Optional


class RegisterType(str, Enum):
    AUSENCIA = "AUSENCIA"
    PRESENCIA = "PRESENCIA"
    TIEMPO_INTERMEDIO = "TIEMPO INTERMEDIO"


class EmployeeHours(SQLModel, table=True):
    __tablename__ = "employee_hours"  # type: ignore

    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    employee_id: Optional[int] = Field(
        default=None,
        foreign_key="employee.id",
        ondelete="CASCADE",
        index=True,
        nullable=True,
    )
    concept_id: Optional[int] = Field(
        default=None, foreign_key="concept.id", nullable=True
    )
    shift_id: int = Field(foreign_key="shift.id")
    check_count: int = Field(default=0)
    work_date: date = Field(default=date.today)
    register_type: RegisterType = Field(default=None)
    first_check_in: Optional[time] = Field(default=None, nullable=True)
    last_check_out: Optional[time] = Field(default=None, nullable=True)
    sumary_time: Optional[time] = Field(default=None, nullable=True)
    extra_hours: Optional[time] = Field(default=None, nullable=True)
    pay: bool = Field(default=False)
    payroll_status: str = Field(
        description="Por pagar, Impagable, Archivado, Pendiente de validación"
    )
    notes: str

    employee: "Employee" = Relationship(back_populates="employee_hours")
    concept: "Concept" = Relationship(back_populates="employee_hours")
    shift: "Shift" = Relationship(back_populates="employee_hours")
