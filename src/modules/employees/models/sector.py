from sqlmodel import Field, SQLModel
from typing import Optional

class Sector(SQLModel, table=True, metadata={"table_name": "sector"}):
    """
    Modelo de Sector para la base de datos.
    """
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    name: str = Field(max_length=100, unique=True, index=True)
    