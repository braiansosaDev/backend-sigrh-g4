from datetime import date
from sqlmodel import SQLModel


class DocumentResponse(SQLModel):
    id: int
    name: str
    extension: str
    creation_date: date
    file: bytes


class DocumentRequest(SQLModel):
    name: str
    extension: str = "pdf"
    creation_date: date
    file: bytes
