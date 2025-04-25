from sqlmodel import Field, Relationship
from schemas.base_schemas import DocumentCreate, WorkHistoryCreate, EmployeeCreate


class Employee(EmployeeCreate, table=True, metadata={"table_name": "employee"}):
    id: int = Field(default=None, primary_key=True)
    work_histories: list["WorkHistory"] = Relationship(back_populates="employee")
    documents: list["Document"] = Relationship(back_populates="employee")


class WorkHistory(
    WorkHistoryCreate, table=True, metadata={"table_name": "work_history"}
):
    id: int = Field(default=None, primary_key=True)
    employee_id: int = Field(foreign_key="employee.id")
    employee: Employee = Relationship(back_populates="work_histories")


class Document(DocumentCreate, table=True, metadata={"table_name": "document"}):
    id: int = Field(default=None, primary_key=True)
    employee_id: int = Field(foreign_key="employee.id")
    employee: Employee = Relationship(back_populates="documents")
