from datetime import date
from typing import Optional
from pydantic import BaseModel
from sqlmodel import Field


class DocumentResponse(BaseModel):
    id: int
    name: str
    extension: str
    creation_date: date
    file: bytes
    active: Optional[bool]
    
class DocumentRequest(BaseModel):
    name: str
    extension: str = "pdf"
    creation_date: date
    file: bytes
    active: Optional[bool]