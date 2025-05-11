from pydantic import BaseModel, Field
from typing import Optional

from src.modules.employees.models.sector import Sector

class JobResponse(BaseModel):
    id: int
    name: str
    sector_id: int
    sector: Optional[Sector]

class CreateJob(BaseModel):
    name: str = Field(max_length=100)
    sector_id: int

class UpdateJob(BaseModel):
    name: Optional[str] = None
    sector_id: int
