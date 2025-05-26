from sqlmodel import Field, SQLModel, Relationship


class Shift(SQLModel, table=True):
    __tablename__ = "shift"  # type: ignore
    id: int = Field(primary_key=True)
    description: str
    type: str
    working_hours: float
    working_days: int

    employee: "Employee" = Relationship(back_populates="shift")
    employee_hours: list["EmployeeHours"] = Relationship(back_populates="shift")
