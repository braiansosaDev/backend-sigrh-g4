from sqlmodel import Field, Relationship, SQLModel
import datetime


class EmployeeHours(SQLModel, table=True):
    __tablename__ = "employee_hours"  # type: ignore
    id: int = Field(primary_key=True)
    employee_id: int = Field(foreign_key="employee.id", nullable=True)
    concept_id: int = Field(foreign_key="concept.id", nullable=True)
    shift_id: int = Field(foreign_key="shift.id", nullable=True)
    weekday: int
    date: datetime.date
    register_type: str
    first_check_in: datetime.time
    last_check_out: datetime.time
    check_count: int
    amount: float
    hours: datetime.time
    pay: bool
    notes: str

    employee: "Employee" = Relationship(back_populates="employee_hours")
