from pydantic import BaseModel, Field
from typing import Optional

class SectorResponse(BaseModel):
    id: int
    name: str

class CreateSector(BaseModel):
    name: str = Field(max_length=100)

class UpdateSector(BaseModel):
    id: int
    name: Optional[str] = None
