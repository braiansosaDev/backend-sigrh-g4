from decimal import Decimal
from typing import Optional
from pydantic import EmailStr, Field, BaseModel, field_validator
from datetime import date
from src.modules.employees.models.country import Country
from src.modules.employees.models.documents import Document
from src.modules.employees.models.job import Job
from src.modules.employees.models.state import State
from src.modules.employees.models.work_history import WorkHistory
from src.modules.employees.schemas.job_models import JobResponse
from src.modules.role.schemas.role_schemas import RolePublic
from src.modules.shift.models.models import Shift

class ChangePasswordRequest(BaseModel):
    employee_id: int
    password: str

class EmployeeResponse(BaseModel):
    """
    Modelo de empleado para la respuesta de un empleado.
    Este modelo se utiliza para serializar los datos de un empleado al enviarlos como respuesta a una solicitud.
    """

    id: int
    user_id: str
    first_name: str
    last_name: str
    dni: str
    type_dni: str
    personal_email: EmailStr
    active: bool
    role_id: Optional[int] = None
    phone: str
    salary: Decimal
    job_id: Optional[int]
    shift_id: Optional[int] = None
    birth_date: date
    hire_date: date
    photo: Optional[bytes]
    address_street: str
    address_city: str
    address_cp: str
    address_state_id: Optional[int]
    address_country_id: Optional[int]
    work_histories: list[WorkHistory]
    documents: list[Document]
    job: Optional[JobResponse] = None
    state: Optional[State] = None
    country: Optional[Country] = None
    shift: Optional[Shift] = None


class MeResponse(BaseModel):
    """
    Modelo de empleado para la respuesta de un empleado.
    Este modelo se utiliza para serializar los datos de un empleado al enviarlos como respuesta a una solicitud.
    """

    id: int
    user_id: str
    first_name: str
    last_name: str
    dni: str
    type_dni: str
    personal_email: EmailStr
    active: bool
    role_id: Optional[int] = None
    phone: str
    salary: Decimal
    job_id: Optional[int]
    birth_date: date
    hire_date: date
    photo: Optional[bytes]
    address_street: str
    address_city: str
    address_cp: str
    address_state_id: Optional[int]
    address_country_id: Optional[int]
    job: Optional[JobResponse] = None
    state: Optional[State] = None
    country: Optional[Country] = None
    role: Optional[RolePublic] = None


class UpdateEmployee(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    dni: Optional[str] = None
    type_dni: Optional[str] = None
    personal_email: Optional[EmailStr] = None
    active: Optional[bool] = None
    role_id: Optional[int] = None
    phone: Optional[str] = None
    salary: Optional[Decimal] = None
    job_id: Optional[int] = None
    birth_date: Optional[date] = None
    hire_date: Optional[date] = None
    photo: Optional[bytes] = None
    address_street: Optional[str] = None
    address_city: Optional[str] = None
    address_cp: Optional[str] = None
    address_state_id: Optional[int] = None
    address_country_id: Optional[int] = None
    work_histories: Optional[list[WorkHistory]] = None
    documents: Optional[list[Document]] = None
    job: Optional["Job"] = None
    state: Optional["State"] = None
    country: Optional["Country"] = None


class CreateEmployee(BaseModel):
    """
    Modelo de empleado para la creación de un nuevo empleado.
    Este modelo se utiliza para validar los datos de entrada al crear un nuevo empleado en la base de datos.
    """

    first_name: str = Field(max_length=100)
    last_name: str = Field(max_length=100)
    dni: str = Field(max_length=50)
    type_dni: str = Field(max_length=10)
    personal_email: EmailStr = Field(max_length=100)
    active: bool = Field(default=False)
    role_id: Optional[int] = None
    password: Optional[str] = None
    phone: str = Field(max_length=20)
    salary: Decimal = Field(gt=0)
    job_id: int
    shift_id: int
    birth_date: date
    hire_date: date = Field(default=date.today())
    photo: Optional[bytes] = Field(default=None)
    address_street: str = Field(max_length=100)
    address_city: str = Field(max_length=100)
    address_cp: str = Field(max_length=100)
    address_state_id: int
    address_country_id: int
    work_histories: Optional[list[WorkHistory]] = None
    documents: Optional[list[Document]] = None

    # Edad mínima (>=16 años)
    @field_validator("birth_date")
    @classmethod
    def check_minimum_age(cls, v):
        today = date.today()
        age = today.year - v.year - ((today.month, today.day) < (v.month, v.day))
        if age < 16:
            raise ValueError("El empleado debe tener al menos 16 años.")
        return v

    # Validación de teléfono: que comience con código de país
    @field_validator("phone")
    @classmethod
    def validate_phone_country_code(cls, v):
        if not v.startswith("+"):
            raise ValueError(
                "El número de teléfono debe incluir el código de país (ej: +54)."
            )
        return v

    # Validación de campos vacíos
    @field_validator(
        "first_name",
        "last_name",
        "dni",
        "type_dni",
        "personal_email",
        "phone",
        "address_street",
        "address_city",
        "address_cp",
        mode="after",
    )
    @classmethod
    def non_empty_strings(cls, v, field):
        if not v.strip():
            raise ValueError(f"El campo '{field.field_name}' no puede estar vacío.")
        return v
