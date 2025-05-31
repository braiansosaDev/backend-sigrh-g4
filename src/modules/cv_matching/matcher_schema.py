from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List, Optional, Any


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
    ability_match: dict[str, Any]
    created_at: datetime
    status: str

    class Config:
        from_attributes = (
            True  # Allows the model to read from SQLModel/SQLAlchemy models
        )


class MatcherResponse(BaseModel):
    postulation_id: Optional[int]
    name: str
    surname: str
    suitable: bool
    ability_match: List[str]
    required_skill_percentage: float
    desirable_skill_percentage: float


class MatcherRequest(BaseModel):
    required_skill_percentage: float
    desirable_skill_percentage: float
