from pydantic import BaseModel
from typing import List, Optional


class MatcherResponse(BaseModel):
    postulation_id: Optional[int]
    name: str
    surname: str
    suitable: bool
    required_words_found: List[str]
    desired_words_found: list[str]
    required_words_not_found: list[str]
    desired_words_not_found: list[str]


class MatcherRequest(BaseModel):
    required_skill_percentage: float
    desirable_skill_percentage: float
