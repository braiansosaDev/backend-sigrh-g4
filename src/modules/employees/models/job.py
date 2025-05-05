from sqlmodel import Field, SQLModel
from typing import Optional

class Job(SQLModel, table=True, metadata={"table_name": "job"}):
    """
    Modelo de puesto o job para la base de datos.
    """
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    name: str = Field(max_length=100, index=True)
    sector_id: str = Field(foreign_key="sector.id")  
