from sqlmodel import Field, Relationship, SQLModel
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from src.modules.employees.models.employee import Employee


class State(SQLModel, table=True):
    """
    Modelo de estado o provincia para la base de datos.
    """

    __tablename__ = "state"  # type: ignore
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    name: str = Field(max_length=100, index=True)
    country_id: int = Field(foreign_key="country.id")

    employees: list["Employee"] = Relationship(back_populates="state", sa_relationship_kwargs={"order_by": "Employee.id"})
