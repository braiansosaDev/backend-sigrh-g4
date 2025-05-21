from sqlmodel import Field, Relationship, SQLModel


class Concept(SQLModel, table=True):
    __tablename__ = "concept"  # type: ignore
    id: int = Field(primary_key=True)
    arca_concept_id: int
    description: str

    employee_hours: "EmployeeHours" = Relationship(back_populates="concept")
