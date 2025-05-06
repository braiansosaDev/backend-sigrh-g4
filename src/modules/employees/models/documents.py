from datetime import date
from typing import TYPE_CHECKING, Optional
from sqlmodel import Field, Relationship, SQLModel
if TYPE_CHECKING:
    from src.modules.employees.models.employee import Employee

class Document(SQLModel, table=True, metadata={"table_name": "document"}):
    """
    Modelo de documento para la base de datos.
    Este modelo representa un documento asociado a un empleado.
    Se utiliza para almacenar información sobre documentos como CV, certificados, etc.
    """
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    employee_id: int = Field(foreign_key="employee.id")
    name: str = Field(max_length=50)
    extension: str = Field(max_length=5)
    creation_date: date
    file: bytes
    active: bool = Field(default=True)
    employee: "Employee" = Relationship(back_populates="documents")
