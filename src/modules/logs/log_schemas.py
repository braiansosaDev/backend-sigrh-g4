from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from .log_model import EntityType


class LogBaseModel(BaseModel):
    description: str
    entity: EntityType
    entity_id: int = Field(gt=0)
    user_id: int = Field(gt=0)


class LogResponse(LogBaseModel):
    id: int
    date_change: datetime


class LogCreateRequest(LogBaseModel):
    pass


class LogUpdateRequest(BaseModel):
    description: Optional[str]
    entity_id: Optional[int] = Field(gt=0)
    user_id: Optional[int] = Field(gt=0)
