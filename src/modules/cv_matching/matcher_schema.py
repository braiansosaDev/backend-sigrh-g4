from pydantic import BaseModel
from typing import Optional


class MatcherResponse(BaseModel):
    postulation_id: Optional[int]
    name: str
    surname: str
    suitable: bool
    required_words_found: list[str]
    desired_words_found: list[str]
    required_words_not_found: list[str]
    desired_words_not_found: list[str]
