from sqlmodel import Field, SQLModel


class Concept(SQLModel, table=True):
    __tablename__ = "concept"  # type: ignore
    id: int = Field(primary_key=True)
    arca_concept_id: int
    description: str
