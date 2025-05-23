from sqlmodel import Field, Relationship, SQLModel


class Concept(SQLModel, table=True):
    __tablename__ = "concept"  # type: ignore
    id: int | None = Field(default=None, primary_key=True)
    # exportation_id: Optional[int]
    description: str = Field(default="")
    is_deletable: bool = Field(default=False)

    employee_hours: "EmployeeHours" = Relationship(back_populates="concept")
