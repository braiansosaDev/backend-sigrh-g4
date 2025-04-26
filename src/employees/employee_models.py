from decimal import Decimal
from typing import Optional
from pydantic import EmailStr, Field
from sqlmodel import SQLModel
from datetime import date


class EmployeeResponse(SQLModel):
    id: int
    email: EmailStr
    phone: str
    dni: str
    full_name: str
    nationality: str
    job_title: str
    department: str
    address: str
    job_title: str
    photo: Optional[bytes]
    hire_date: date
    birth_date: date


class UpdateEmployee(SQLModel):
    phone: Optional[str] = Field(unique=True, max_length=20)
    address: Optional[str] = Field(max_length=200)
    photo: Optional[bytes] = Field(default=None)
    facial_register: Optional[bytes] = Field(default=None)
    salary: Optional[Decimal] = Field(gt=0)


# class DeleteEmployee(SQLModel):
#     id: UUID


class CreateEmployee(SQLModel):
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


# class LoginRequest(SQLModel):
#     email: EmailStr = Field(max_length=100)
#     password: str = Field(max_length=100)
