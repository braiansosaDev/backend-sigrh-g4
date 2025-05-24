from datetime import date, time
from pydantic import BaseModel


class PayrollRequest(BaseModel):
    employee_id: int
    start_date: date
    end_date: date


class ConceptSchema(BaseModel):
    id: int | None
    description: str
    is_deletable: bool

    model_config = {"from_attributes": True}


class ShiftSchema(BaseModel):
    id: int
    description: str
    type: str
    working_hours: float
    working_days: int

    model_config = {"from_attributes": True}


class EmployeeHoursSchema(BaseModel):
    id: int | None
    employee_id: int | None
    concept_id: int | None
    shift_id: int
    check_count: int
    work_date: date
    register_type: str
    first_check_in: time | None
    last_check_out: time | None
    time_worked: time | None
    extra_hours: time | None
    pay: bool
    notes: str

    model_config = {"from_attributes": True}


class PayrollResponse(BaseModel):
    employee_hours: EmployeeHoursSchema
    concept: ConceptSchema
    shift: ShiftSchema
