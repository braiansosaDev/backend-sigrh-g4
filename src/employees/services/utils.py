from typing import List
from sqlmodel import select
from src.database.core import DatabaseSession
from src.schemas.entities import Document, Employee, WorkHistory


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
