from datetime import date
from typing import TYPE_CHECKING, Optional
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from src.modules.employees.models.employee import Employee


class WorkHistory(SQLModel, table=True):
    """
    Modelo de historial laboral para la base de datos.
    Este modelo representa el historial laboral de un empleado.
    Se utiliza para almacenar información sobre los trabajos anteriores de un empleado,
    """

    __tablename__ = "work_history"  # type: ignore
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    employee_id: int = Field(foreign_key="employee.id", ondelete="CASCADE")
    job_id: int = Field(foreign_key="job.id")
    from_date: date
    to_date: date
    company_name: str = Field(max_length=40, index=True)
    notes: str = Field(max_length=100)

    employee: "Employee" = Relationship(back_populates="work_histories")
