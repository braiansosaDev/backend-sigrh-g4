from pydantic import BaseModel, Field
from typing import Optional

class JobResponse(BaseModel):
    id: int
    name: str
    sector_id: int

class CreateJob(BaseModel):
    name: str = Field(max_length=100)
    sector_id: int

class UpdateJob(BaseModel):
    name: Optional[str] = None
    sector_id: int
