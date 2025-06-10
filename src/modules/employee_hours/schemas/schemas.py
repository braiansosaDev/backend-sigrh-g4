from typing import Optional
from pydantic import BaseModel
from datetime import date, time
from enum import Enum


class RegisterType(str, Enum):
    AUSENCIA = "AUSENCIA"
    PRESENCIA = "PRESENCIA"
    DIA_NO_HABIL = "DIA NO HABIL"

class EmployeeHoursPatchRequest(BaseModel):
    employee_id: Optional[int] = None
    concept_id: Optional[int] = None
    shift_id: Optional[int] = None
    check_count: Optional[int] = None
    notes: Optional[str] = None
    register_type: Optional[RegisterType] = None
    first_check_in: Optional[time] = None
    last_check_out: Optional[time] = None
    sumary_time: Optional[time] = None
    work_date: Optional[date] = None
    payroll_status: Optional[str] = None


class EmployeeHoursPatchResponse(BaseModel):
    employee_id: Optional[int] = None
    concept_id: Optional[int] = None
    shift_id: Optional[int] = None
    check_count: Optional[int] = None
    notes: Optional[str] = None
    register_type: Optional[RegisterType] = None
    first_check_in: Optional[time] = None
    last_check_out: Optional[time] = None
    sumary_time: Optional[time] = None
    work_date: Optional[date] = None
    payroll_status: Optional[str] = None


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
    payroll_status: str


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
    payroll_status: str
