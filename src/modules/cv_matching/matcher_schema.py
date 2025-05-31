from pydantic import BaseModel
from typing import List, Optional


class MatcherResponse(BaseModel):
    postulation_id: Optional[int]
    name: str
    surname: str
    suitable: bool
    ability_match: List[str]
    abilities_not_found: list[str]
    required_skill_percentage: float
    desirable_skill_percentage: float


class MatcherRequest(BaseModel):
    required_skill_percentage: float
    desirable_skill_percentage: float
