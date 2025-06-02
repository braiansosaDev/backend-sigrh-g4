from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime
from src.modules.clock_events.schemas.schemas import ClockEventTypes
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.modules.employees.models.employee import Employee


class ClockEvents(SQLModel, table=True):
    __tablename__ = "clock_events"  # type: ignore
    id: int = Field(primary_key=True)
    employee_id: int = Field(
        foreign_key="employee.id", nullable=True, ondelete="CASCADE"
    )
    event_date: datetime
    event_type: ClockEventTypes
    source: str
    device_id: str

    employee: "Employee" = Relationship(back_populates="clock_events")
