from datetime import date
from decimal import Decimal
from typing import Optional
from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel
from src.modules.employees.models.documents import Document
from src.modules.employees.models.work_history import WorkHistory

class Employee(SQLModel, table=True, metadata={"table_name": "employee"}):
    """
    Modelo de empleado para la base de datos.
    """

    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    # work_histories: list["WorkHistory"] = Relationship(back_populates="employee")
    # documents: list["Document"] = Relationship(back_populates="employee")
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
