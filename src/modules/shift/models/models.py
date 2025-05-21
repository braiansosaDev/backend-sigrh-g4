from sqlmodel import Field, SQLModel


class Shift(SQLModel, table=True):
    __tablename__ = "shift"  # type: ignore
    id: int = Field(primary_key=True)
    description: str
    type: str
    working_hours: float
    working_days: int
