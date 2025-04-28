from datetime import date
from decimal import Decimal
from typing import Optional
from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel
from src.schemas.employee_models import CreateEmployee


class Employee(CreateEmployee, table=True, metadata={"table_name": "employee"}):
    """
    Modelo de empleado para la base de datos.
    """

    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    work_histories: list["WorkHistory"] = Relationship(back_populates="employee")
    documents: list["Document"] = Relationship(back_populates="employee")
    dni: str = Field(unique=True, max_length=50)
    email: EmailStr = Field(unique=True, max_length=100)
    phone: str = Field(unique=True, max_length=20)
    full_name: str = Field(max_length=100)
    password: str = Field(max_length=100)
    nationality: str = Field(max_length=50, index=True)
    job_title: str = Field(max_length=100)
    department: str = Field(max_length=100)
    address: str = Field(max_length=200)
    photo: Optional[bytes] = Field(default=None)
    facial_register: Optional[bytes] = Field(default=None)
    hire_date: date = Field(default=date.today())
    birth_date: date  # Agregar restricciones
    salary: Decimal = Field(gt=0)


class WorkHistory(SQLModel, table=True, metadata={"table_name": "work_history"}):
    """
    Modelo de historial laboral para la base de datos.
    Este modelo representa el historial laboral de un empleado.
    Se utiliza para almacenar información sobre los trabajos anteriores de un empleado,
    """

    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    employee_id: int = Field(foreign_key="employee.id")
    employee: Employee = Relationship(back_populates="work_histories")
    job_title: str = Field(max_length=100)
    from_date: date
    to_date: date
    company_name: str = Field(max_length=40, index=True)
    notes: str = Field(max_length=1000)


class Document(SQLModel, table=True, metadata={"table_name": "document"}):
    """
    Modelo de documento para la base de datos.
    Este modelo representa un documento asociado a un empleado.
    Se utiliza para almacenar información sobre documentos como CV, certificados, etc.
    """

    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    employee_id: int = Field(foreign_key="employee.id")
    employee: Employee = Relationship(back_populates="documents")
    name: str = Field(max_length=50)
    extension: str = Field(max_length=5)
    creation_date: date
    file: bytes
