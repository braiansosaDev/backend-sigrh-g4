from pydantic import BaseModel


class ConceptRequest(BaseModel):
    exportation_id: int
    description: str
    is_deletable: bool = False


class ConceptResponse(BaseModel):
    id: int
    exportation_id: int
    description: str
    is_deletable: bool
