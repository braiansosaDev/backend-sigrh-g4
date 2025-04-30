from decimal import Decimal
from typing import Optional
from pydantic import EmailStr, Field, BaseModel
from datetime import date


class EmployeeResponse(BaseModel):
    """
    Modelo de empleado para la respuesta de un empleado.
    Este modelo se utiliza para serializar los datos de un empleado al enviarlos como respuesta a una solicitud.
    """

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
    salary: Decimal
    password: str


class UpdateEmployee(BaseModel):
    phone: Optional[str] = None
    address: Optional[str] = None
    photo: Optional[bytes] = None
    facial_register: Optional[bytes] = None
    salary: Optional[Decimal] = None
    full_name: Optional[str] = None
    job_title: Optional[str] = None
    dni: Optional[str] = None
    email: Optional[EmailStr] = None
    hire_date: Optional[date] = None
    birth_date: Optional[date] = None
    password: Optional[str] = None


class CreateEmployee(BaseModel):
    """
    Modelo de empleado para la creación de un nuevo empleado.
    Este modelo se utiliza para validar los datos de entrada al crear un nuevo empleado en la base de datos.
    """

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
    birth_date: date
    salary: Decimal = Field(gt=0)
