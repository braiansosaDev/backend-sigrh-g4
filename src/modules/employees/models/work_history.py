from datetime import date
from decimal import Decimal
from typing import Optional
from sqlmodel import Field, SQLModel

class WorkHistory(SQLModel, table=True, metadata={"table_name": "work_history"}):
    """
    Modelo de historial laboral para la base de datos.
    Este modelo representa el historial laboral de un empleado.
    Se utiliza para almacenar información sobre los trabajos anteriores de un empleado,
    """

    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    employee_id: int = Field(foreign_key="employee.id")
    job_id: int = Field(foreign_key="job.id")
    from_date: date
    to_date: date
    company_name: str = Field(max_length=40, index=True)
    notes: str = Field(max_length=100)