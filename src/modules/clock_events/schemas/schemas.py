from typing import Optional
from pydantic import BaseModel
from datetime import datetime, date, timedelta, timezone
from enum import Enum


class ClockEventTypes(str, Enum):
    IN = "in"
    OUT = "out"


class ClockEventRequest(BaseModel):
    employee_id: int
    device_id: Optional[str] = None
    source: Optional[str] = None
    event_type: ClockEventTypes
    event_date: datetime = datetime.now(timezone.utc).astimezone(
        timezone(timedelta(hours=-3))
    )


class JobRead(BaseModel):
    id: int
    name: str


class EmployeeRead(BaseModel):
    id: int
    first_name: str
    last_name: str
    job: Optional[JobRead]  # Relación anidada


class ClockEventResponse(BaseModel):
    employee_id: int
    device_id: Optional[str] = None
    source: Optional[str] = None
    event_type: ClockEventTypes
    event_date: datetime = datetime.now(timezone.utc).astimezone(
        timezone(timedelta(hours=-3))
    )
    employee: Optional[EmployeeRead]


class ClockEventRead(BaseModel):
    id: int
    event_date: datetime = datetime.now(timezone.utc).astimezone(
        timezone(timedelta(hours=-3))
    )
    event_type: str
    source: str
    device_id: str
    employee: Optional[EmployeeRead]


class ClockEventAttendanceSummary(BaseModel):
    employee_id: int
    first_name: str
    last_name: str
    job: Optional[str] = None
    date: Optional[date]
    first_in: Optional[datetime] = None
    last_out: Optional[datetime] = None
    total_events: int
