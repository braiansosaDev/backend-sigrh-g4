from typing import Optional
from sqlmodel import Field, Relationship, SQLModel
from datetime import datetime
from src.modules.clock_events.schemas.schemas import ClockEventTypes
from src.modules.employees.models.employee import Employee


class ClockEvents(SQLModel, table=True):
    __tablename__ = "clock_events"  # type: ignore
    id: int = Field(primary_key=True)
    employee_id: int = Field(foreign_key="employee.id", nullable=True)
    event_date: datetime
    event_type: ClockEventTypes
    source: str
    device_id: str

    employee: Optional["Employee"] = Relationship()
