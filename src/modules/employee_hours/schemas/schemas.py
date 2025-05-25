from pydantic import BaseModel, Field
from datetime import date, time


class EmployeeHoursRequest(BaseModel):
    employee_id: int
    concept_id: int
    shift_id: int
    weekday: int = Field(ge=1, le=7)
    check_count: int
    notes: str
    register_type: str  # ESPECIFICAR!
    first_check_in: time
    last_check_out: time
    hours: time
    date: date
    amount: float
    pay: bool


class EmployeeHoursResponse(BaseModel):
    id: int
    employee_id: int
    concept_id: int
    shift_id: int
    weekday: int = Field(ge=1, le=7)
    check_count: int
    notes: str
    register_type: str  # ESPECIFICAR!
    first_check_in: time
    last_check_out: time
    hours: time
    date: date
    amount: float
    pay: bool
