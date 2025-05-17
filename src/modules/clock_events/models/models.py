from sqlmodel import Field, SQLModel
from datetime import datetime
from src.modules.clock_events.schemas.schemas import ClockEventTypes


class ClockEvents(SQLModel, table=True):
    __tablename__ = "clock_events"  # type: ignore
    id: int = Field(primary_key=True)
    employee_id: int = Field(foreign_key="employee.id", nullable=True)
    event_date: datetime
    event_type: ClockEventTypes
    source: str
    device_id: str
