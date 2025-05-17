from pydantic import BaseModel
from datetime import datetime
from enum import Enum


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
