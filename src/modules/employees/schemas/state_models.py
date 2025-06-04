from pydantic import BaseModel, Field
from typing import Optional

class StateResponse(BaseModel):
    id: int
    name: str
    country_id: int

class CreateState(BaseModel):
    name: str = Field(max_length=100)
    country_id: int

class UpdateState(BaseModel):
    name: Optional[str] = None
    country_id: Optional[int] = None
