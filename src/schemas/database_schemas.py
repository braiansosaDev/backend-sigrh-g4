from sqlmodel import Field, Relationship
from schemas.base_schemas import DocumentBase, WorkHistoryBase, EmployeeBase


class Employee(EmployeeBase, table=True):
    id: int = Field(default=None, primary_key=True)
    work_histories: list["WorkHistory"] = Relationship(back_populates="employee")
    documents: list["Document"] = Relationship(back_populates="employee")


class WorkHistory(WorkHistoryBase, table=True):
    id: int = Field(default=None, primary_key=True)
    employee_id: int = Field(foreign_key="employee.id")
    employee: Employee = Relationship(back_populates="work_histories")


class Document(DocumentBase, table=True):
    id: int = Field(default=None, primary_key=True)
    employee_id: int = Field(foreign_key="employee.id")
    employee: Employee = Relationship(back_populates="documents")
