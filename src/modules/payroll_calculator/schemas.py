from datetime import date, time
from typing import List, Optional
from pydantic import BaseModel

from src.modules.employees.models.employee import Employee

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
    sumary_time: time | None
    extra_hours: time | None
    payroll_status: str
    notes: str

    model_config = {"from_attributes": True}

class PayrollResponse(BaseModel):
    employee_hours: EmployeeHoursSchema
    concept: ConceptSchema
    shift: ShiftSchema

class PayrollPendingValidationRequest(BaseModel):
    employee_id: Optional[List[int]] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None

class PayrollPendingValidationResponse(BaseModel):
    employee: Employee
    employee_hours: EmployeeHoursSchema
    concept: ConceptSchema
    shift: ShiftSchema
