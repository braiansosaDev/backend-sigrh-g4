from sqlmodel import Field, Relationship, SQLModel
from sqlalchemy import Column, Integer


class Concept(SQLModel, table=True):
    __tablename__ = "concept"  # type: ignore
    id: int = Field(primary_key=True)
    exportation_id: int = Field(
        default=None, sa_column=Column(Integer, autoincrement=True, unique=True)
    )
    description: str = Field(default="")
    is_deletable: bool = Field(default=False)

    employee_hours: "EmployeeHours" = Relationship(back_populates="concept")
