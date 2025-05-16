from sqlmodel import Field, SQLModel
from datetime import datetime


class ClockEvents(SQLModel, table=True):
    __tablename__ = "clock_events"  # type: ignore
    id: int = Field(primary_key=True)
    employee_id: int = Field(foreign_key="employee.id", nullable=True)
    event_date: datetime
    event_type: datetime
    source: str
    device_id: int
