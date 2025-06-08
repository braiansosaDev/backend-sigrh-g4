from sqlalchemy import func, Column, TIMESTAMP
from sqlmodel import SQLModel, Field, Relationship
from datetime import date
from pydantic import AwareDatetime
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from src.modules.employees.models.employee import Employee


class LeaveType(SQLModel, table=True):
    __tablename__ = "leave_type"  # type: ignore

    id: Optional[int] = Field(primary_key=True, index=True, default=None)
    type: str = Field(min_length=1, unique=True, index=True)
    justification_required: bool = Field(default=False)


class Leave(SQLModel, table=True):
    __tablename__ = "leave"  # type: ignore

    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    employee_id: int = Field(foreign_key="employee.id", index=True)
    request_date: date = Field(default_factory=date.today, index=True)
    start_date: date = Field(index=True)
    end_date: date = Field(index=True)
    file: Optional[str] = Field(default=None)

    leave_type_id: int = Field(foreign_key="leave_type.id")
    leave_type: LeaveType = Relationship()

    reason: Optional[str] = Field(default=None)

    document_status: str = Field(
        index=True, description="Ej: No requerido, Validación, Aprobado, Rechazado"
    )

    request_status: str = Field(
        index=True, description="Ej: Pendiente, Aprobado, Rechazado"
    )

    observations: Optional[str] = Field(default=None)

    created_at: Optional[AwareDatetime] = Field(
        default=None,
        sa_column=Column(
            TIMESTAMP(timezone=True), nullable=False, server_default=func.now()
        ),
    )
    updated_at: Optional[AwareDatetime] = Field(
        default=None,
        sa_column=Column(
            TIMESTAMP(timezone=True), nullable=False, server_default=func.now()
        ),
    )

    employee: "Employee" = Relationship(back_populates="leaves")
