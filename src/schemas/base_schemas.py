from datetime import date
from decimal import Decimal
from typing import Optional
from sqlmodel import Field, SQLModel


class EmployeeBase(SQLModel):  # Definir alcance
    password: str = Field(
        max_length=100
    )  # Podriamos almacenar el hash de la contraseña
    salary: Decimal
    facial_register: Optional[bytes] = Field(default=None)
    photo: Optional[bytes] = Field(default=None)


class EmployeeCreate(EmployeeBase):
    full_name: str = Field(max_length=100)
    nationality: str = Field(max_length=50, index=True)
    job_title: str = Field(max_length=100)
    department: str = Field(max_length=100)
    phone: str = Field(unique=True, max_length=20)
    email: str = Field(unique=True, max_lenght=100)
    address: str = Field(max_length=200)
    dni: str = Field(unique=True, max_length=50)
    hire_date: date
    birth_date: date


class WorkHistoryBase(SQLModel):  # Definir alcance
    pass


class WorkHistoryCreate(WorkHistoryBase):
    job_title: str
    from_date: date
    to_date: date
    company_name: str = Field(max_length=40, index=True)
    notes: str = Field(max_length=1000)


class DocumentBase(SQLModel):  # Definir alcance
    pass


class DocumentCreate(DocumentBase):
    name: str = Field(max_length=50)
    extension: str = Field(max_length=5)
    creation_date: date
    file: bytes
