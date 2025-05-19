from typing import Optional
from pydantic import BaseModel
from datetime import datetime
from enum import Enum

from src.modules.employees.models.employee import Employee


class ClockEventTypes(str, Enum):
    IN = "in"
    OUT = "out"


class ClockEventRequest(BaseModel):
    employee_id: int
    device_id: str
    source: str
    event_type: ClockEventTypes
    event_date: datetime


class ClockEventResponse(BaseModel):
    employee_id: int
    device_id: str
    source: str
    event_type: ClockEventTypes
    event_date: datetime
    employee: Employee

class JobRead(BaseModel):
    id: int
    name: str

class EmployeeRead(BaseModel):
    id: int
    first_name: str
    last_name: str
    job: Optional[JobRead]  # Relación anidada

class ClockEventRead(BaseModel):
    id: int
    event_date: datetime
    event_type: str
    source: str
    device_id: str
    employee: Optional[EmployeeRead]

class ClockEventAttendanceSummary(BaseModel):
    employee_id: int
    first_name: str
    last_name: str
    job: Optional[str] = None
    first_in: Optional[datetime] = None
    last_out: Optional[datetime] = None
    total_events: int
