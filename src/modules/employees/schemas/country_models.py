from pydantic import BaseModel, Field
from typing import Optional

class CountryResponse(BaseModel):
    id: int
    name: str

class CreateCountry(BaseModel):
    name: str = Field(max_length=100)

class UpdateCountry(BaseModel):
    name: Optional[str] = None
