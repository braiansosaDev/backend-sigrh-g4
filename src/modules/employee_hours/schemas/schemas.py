from pydantic import BaseModel
from datetime import date, time
from enum import Enum


class RegisterType(str, Enum):
    AUSENCIA = "AUSENCIA"
    PRESENCIA = "PRESENCIA"
    TIEMPO_INTERMEDIO = "TIEMPO INTERMEDIO"


class EmployeeHoursRequest(BaseModel):
    employee_id: int
    concept_id: int
    shift_id: int
    check_count: int
    notes: str
    register_type: RegisterType
    first_check_in: time
    last_check_out: time
    sumary_time: time
    work_date: date
    pay: bool


class EmployeeHoursResponse(BaseModel):
    id: int
    employee_id: int
    concept_id: int
    shift_id: int
    check_count: int
    notes: str
    register_type: RegisterType
    first_check_in: time
    last_check_out: time
    sumary_time: time
    work_date: date
    pay: bool
