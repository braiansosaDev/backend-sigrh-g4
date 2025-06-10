from sqlmodel import Field, Relationship, SQLModel
from datetime import time, date
from enum import Enum
from typing import Optional
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.modules.employees.models.employee import Employee
    from src.modules.concept.models.models import Concept
    from src.modules.shift.models.models import Shift


class RegisterType(str, Enum):
    AUSENCIA = "AUSENCIA"
    PRESENCIA = "PRESENCIA"
    DIA_NO_HABIL = "DIA NO HABIL"

class payType(str, Enum):
    PAYABLE = "payable"
    NOT_PAYABLE = "not payable"
    ARCHIVED = "archived"
    PENDING_VALIDATION = "pending validation"

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
    first_check_in: Optional[time] = Field(default=None, nullable=True)
    last_check_out: Optional[time] = Field(default=None, nullable=True)
    sumary_time: Optional[time] = Field(default=None, nullable=True)
    extra_hours: Optional[time] = Field(default=None, nullable=True)
    payroll_status: payType = Field(default=None)
    notes: str

    employee: "Employee" = Relationship(back_populates="employee_hours")
    concept: "Concept" = Relationship(back_populates="employee_hours")
    shift: "Shift" = Relationship(back_populates="employee_hours")
