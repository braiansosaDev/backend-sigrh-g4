from datetime import datetime
from enum import StrEnum
from sqlmodel import Field, SQLModel


class EntityType(StrEnum):
    LICENCIA = "LICENCIA"
    NOMINA = "NOMINA"
    CONVOCATORIA = "CONVOCATORIA"


class Log(SQLModel, table=True):
    __tablename__: str = "logs"  # type: ignore

    id: int = Field(primary_key=True, index=True)
    entity_id: int
    user_id: int
    entity: EntityType
    date_change: datetime = Field(default_factory=datetime.now)
    description: str = Field(default="")
