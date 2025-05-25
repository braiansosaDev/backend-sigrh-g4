from pydantic import BaseModel


class ShiftRequest(BaseModel):
    description: str
    type: str


class ShiftResponse(BaseModel):
    id: int
    description: str
    type: str
