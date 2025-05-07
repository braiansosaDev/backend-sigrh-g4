from sqlmodel import Field, SQLModel
from typing import Optional

class State(SQLModel, table=True, metadata={"table_name": "state"}):
    """
    Modelo de estado o provincia para la base de datos.
    """
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    name: str = Field(max_length=100, index=True)
    country_id: int = Field(foreign_key="country.id")
