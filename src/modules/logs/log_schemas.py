from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from .log_model import EntityType

class LogBaseModel(BaseModel):
    description: str
    entity: EntityType
    entity_id: int = Field(gt=0)
    user_id: int = Field(gt=0)

class EmployeeBrief(BaseModel):
    id: int
    first_name: str
    last_name: str


class LogResponse(LogBaseModel):
    id: int
    date_change: datetime
    employee: Optional[EmployeeBrief] = None


class LogCreateRequest(LogBaseModel):
    pass


class LogUpdateRequest(BaseModel):
    description: Optional[str]
    entity_id: Optional[int] = Field(gt=0)
    user_id: Optional[int] = Field(gt=0)
