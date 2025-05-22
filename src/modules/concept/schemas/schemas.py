from pydantic import BaseModel


class ConceptRequest(BaseModel):
    arca_concept_id: int
    description: str


class ConceptResponse(BaseModel):
    id: int
    arca_concept_id: int
    description: str
