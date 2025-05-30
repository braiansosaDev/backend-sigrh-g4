from sqlmodel import SQLModel, Field
from datetime import date
from typing import Optional


class Leave(SQLModel, table=True):
    __tablename__ = "leave"  # type: ignore

    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    employee_id: int = Field(foreign_key="employee.id", index=True)
    request_date: date = Field(default_factory=date.today, index=True)
    start_date: date = Field(index=True)
    end_date: date = Field(index=True)

    leave_type: str = Field(
        index=True, description="Ej: Médica, Académica, Personal, Casamiento, etc."
    )
    reason: Optional[str] = Field(default=None)

    document_status: str = Field(
        index=True, description="Ej: No requerido, Validación, Aprobado, Rechazado"
    )

    request_status: str = Field(
        index=True, description="Ej: Pendiente, Aprobado, Rechazado"
    )

    observations: Optional[str] = Field(default=None)
