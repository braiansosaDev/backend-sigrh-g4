from datetime import date
from decimal import Decimal
from typing import Optional
from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.modules.clock_events.models.models import ClockEvents
    from src.modules.employee_hours.models.models import EmployeeHours
    from src.modules.employees.models.country import Country
    from src.modules.employees.models.documents import Document
    from src.modules.employees.models.job import Job
    from src.modules.employees.models.state import State
    from src.modules.employees.models.work_history import WorkHistory
    from src.modules.opportunity.models.job_opportunity_models import (
        JobOpportunityModel,
    )
    from src.modules.face_recognition.models.face_recognition import FaceRecognition
    from src.modules.shift.models.models import Shift
    from src.modules.role.models.role_models import Role
    from src.modules.leave.models.leave_models import Leave


class Employee(SQLModel, table=True):
    """
    Modelo de empleado para la base de datos.
    """

    __tablename__: str = "employee"  # type: ignore

    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    user_id: str = Field(unique=True, max_length=100)
    first_name: str = Field(max_length=100)
    last_name: str = Field(max_length=100)
    dni: str = Field(unique=True, max_length=50)
    type_dni: str = Field(max_length=10)
    personal_email: EmailStr = Field(unique=True, max_length=100)
    active: bool = Field(default=False)
    role_id: int | None = Field(foreign_key="role.id", default=None)
    password: str | None = Field(max_length=100, nullable=True)
    phone: str = Field(unique=True, max_length=20)
    salary: Decimal = Field(gt=0)
    job_id: int = Field(foreign_key="job.id", nullable=True)
    birth_date: date  # Agregar restricciones
    hire_date: date = Field(default=date.today())
    photo: Optional[bytes] = Field(default=None)
    address_street: str = Field(max_length=100)
    address_city: str = Field(max_length=100)
    address_cp: str = Field(max_length=100)
    address_state_id: int = Field(foreign_key="state.id", nullable=True)
    address_country_id: int = Field(foreign_key="country.id", nullable=True)
    shift_id: int = Field(foreign_key="shift.id", nullable=True)

    role: Optional["Role"] = Relationship()
    job: Optional["Job"] = Relationship(back_populates="employees")
    state: Optional["State"] = Relationship(back_populates="employees")
    country: Optional["Country"] = Relationship(back_populates="employees")
    shift: "Shift" = Relationship(back_populates="employees")
    face_recognition: Optional["FaceRecognition"] = Relationship(
        back_populates="employee"
    )

    work_histories: list["WorkHistory"] = Relationship(
        back_populates="employee",
        cascade_delete=True,
        sa_relationship_kwargs={"order_by": "WorkHistory.id"},
    )
    documents: list["Document"] = Relationship(
        back_populates="employee",
        cascade_delete=True,
        sa_relationship_kwargs={"order_by": "Document.id"},
    )
    employee_hours: list["EmployeeHours"] = Relationship(
        back_populates="employee",
        cascade_delete=True,
        sa_relationship_kwargs={"order_by": "EmployeeHours.id"},
    )
    clock_events: list["ClockEvents"] = Relationship(
        back_populates="employee",
        cascade_delete=True,
        sa_relationship_kwargs={"order_by": "ClockEvents.id"},
    )
    job_opportunity: list["JobOpportunityModel"] = Relationship(
        back_populates="employee",
        cascade_delete=True,
        sa_relationship_kwargs={"order_by": "JobOpportunityModel.id"},
    )
    leaves: list["Leave"] = Relationship(
        back_populates="employee",
        cascade_delete=True,
        sa_relationship_kwargs={"order_by": "Leave.id"},
    )
