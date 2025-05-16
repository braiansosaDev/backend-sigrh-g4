from datetime import date
from decimal import Decimal
from typing import Optional
from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel
from src.modules.employee_hours.models.models import EmployeeHours
from src.modules.employees.models.country import Country
from src.modules.employees.models.documents import Document
from src.modules.employees.models.job import Job
from src.modules.employees.models.state import State
from src.modules.employees.models.work_history import WorkHistory


class Employee(SQLModel, table=True, metadata={"table_name": "employee"}):
    """
    Modelo de empleado para la base de datos.
    """

    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    user_id: str = Field(unique=True, max_length=100)
    first_name: str = Field(max_length=100)
    last_name: str = Field(max_length=100)
    dni: str = Field(unique=True, max_length=50)
    type_dni: str = Field(max_length=10)
    personal_email: EmailStr = Field(unique=True, max_length=100)
    active: bool = Field(default=False)
    role: str = Field(max_length=100, nullable=True)
    password: str = Field(max_length=100, nullable=True)
    phone: str = Field(unique=True, max_length=20)
    salary: Decimal = Field(gt=0)
    job_id: int = Field(foreign_key="job.id", nullable=True)
    birth_date: date  # Agregar restricciones
    hire_date: date = Field(default=date.today())
    photo: Optional[bytes] = Field(default=None)
    facial_register: Optional[bytes] = Field(default=None)
    address_street: str = Field(max_length=100)
    address_city: str = Field(max_length=100)
    address_cp: str = Field(max_length=100)
    address_state_id: int = Field(foreign_key="state.id", nullable=True)
    address_country_id: int = Field(foreign_key="country.id", nullable=True)

    work_histories: list["WorkHistory"] = Relationship(back_populates="employee")
    documents: list["Document"] = Relationship(back_populates="employee")
    job: Optional["Job"] = Relationship(back_populates="employee")
    state: Optional["State"] = Relationship(back_populates="employee")
    country: Optional["Country"] = Relationship(back_populates="employee")
    employee_hours: Optional["EmployeeHours"] = Relationship(back_populates="employee")
