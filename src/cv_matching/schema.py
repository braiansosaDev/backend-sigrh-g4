from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List


class PostulationResponse(BaseModel):
    id: int
    job_opportunity_id: int | None
    name: str
    surname: str
    email: EmailStr
    phone_number: int
    address_country_id: int | None
    address_state_id: int | None
    cv_file: str
    evaluated_at: datetime
    suitable: bool
    ability_match: dict
    created_at: datetime
    status: str

    class Config:
        from_attributes = (
            True  # Allows the model to read from SQLModel/SQLAlchemy models
        )


class MatcherResponse(BaseModel):
    postulation_id: int
    name: str
    surname: str
    suitable: bool
    ability_match: List[str]
