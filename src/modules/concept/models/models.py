from sqlmodel import Field, Relationship, SQLModel


class Concept(SQLModel, table=True):
    __tablename__ = "concept"  # type: ignore
    id: int = Field(primary_key=True)
    exportation_id: int
    description: str = Field(default="")
    is_deletable: bool = Field(default=False)

    employee_hours: "EmployeeHours" = Relationship(back_populates="concept")
