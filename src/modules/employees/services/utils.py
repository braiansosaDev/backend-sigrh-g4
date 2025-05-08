from typing import List
from fastapi import HTTPException, status
from sqlmodel import select
from src.database.core import DatabaseSession
from src.modules.employees.models.documents import Document
from src.modules.employees.models.employee import Employee
from src.modules.employees.models.work_history import WorkHistory
from src.modules.employees.schemas.employee_models import CreateEmployee

def get_single_work_history_by_id(
    db: DatabaseSession, employee_id: int, work_history_id: int
) -> WorkHistory:
    return db.exec(
        select(WorkHistory)
        .where(WorkHistory.id == work_history_id)
        .where(WorkHistory.employee_id == employee_id)
    ).one_or_none()

def get_work_history_of_employee(
    db: DatabaseSession,
    employee_id: int,
) -> List[WorkHistory]:
    return db.exec(
        select(WorkHistory).where(WorkHistory.employee_id == employee_id)
    ).all()

def get_documents_of_employee(
    db: DatabaseSession,
    employee_id: int,
) -> List[Document]:
    return db.exec(select(Document).where(Document.employee_id == employee_id)).all()


def get_document(db: DatabaseSession, document_id: int, employee_id: int):
    return db.exec(
        select(Document)
        .where(Document.id == document_id)
        .where(Document.employee_id == employee_id)
    ).one_or_none()


def get_employee_by_id(db: DatabaseSession, employee_id: int) -> Employee:
    """
    Obtiene todos los empleados de la base de datos.
    Args:
    db (Session): Sesión de la base de datos.
    id (int): ID del empleado a buscar.
    Returns:
    Employee: Empleado encontrado.
    """
    return db.exec(select(Employee).where(Employee.id == employee_id)).one_or_none()

def get_employee_by_user_id(db: DatabaseSession, user_id: str) -> Employee:
    return db.exec(select(Employee).where(Employee.user_id == user_id)).one_or_none()

def get_all_employees(db: DatabaseSession):
    return db.exec(select(Employee)).all()

def create_user_id(db: DatabaseSession, employee_request: CreateEmployee) -> str:
    first_char = employee_request.first_name[0].lower()
    last_name = employee_request.last_name.lower()
    dni = employee_request.dni[-3:]
    new_user_id = f"{first_char}{last_name}{dni}"

    if db.exec(select(Employee).where(Employee.user_id == new_user_id)).one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User ID already exists.",
        )

    return new_user_id