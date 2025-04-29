from datetime import date
from pydantic import BaseModel


class DocumentResponse(BaseModel):
    id: int
    name: str
    extension: str
    creation_date: date
    file: bytes


class DocumentRequest(BaseModel):
    name: str
    extension: str = "pdf"
    creation_date: date
    file: bytes
