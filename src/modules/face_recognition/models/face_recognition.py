from sqlmodel import JSON, Column, Field, Relationship, SQLModel
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from src.modules.employees.models.employee import Employee

class FaceRecognition(SQLModel, table=True, metadata={"table_name": "face_recognition"}):
    """
    Modelo de registro facial para la base de datos.
    """
    __tablename__ = "face_recognition"  # type: ignore

    id: Optional[int] = Field(primary_key=True, index=True)
    employee_id: int = Field(foreign_key="employee.id")
    embedding: Optional[list[float]] = Field(sa_column=Column(JSON))
    employee: "Employee" = Relationship(back_populates="face_recognition")
