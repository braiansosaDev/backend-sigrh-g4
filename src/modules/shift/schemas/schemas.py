from pydantic import BaseModel


class ShiftRequest(BaseModel):
    description: str
    type: str
    working_hours: float
    working_days: int


class ShiftResponse(BaseModel):
    id: int
    description: str
    type: str
    working_hours: float
    working_days: int
