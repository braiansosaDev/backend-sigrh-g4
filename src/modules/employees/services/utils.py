from typing import Sequence, cast, Any, Optional
from fastapi import HTTPException, status
from sqlmodel import func, select
from src.database.core import DatabaseSession
from src.modules.employees.models.documents import Document
from src.modules.employees.models.employee import Employee
from src.modules.employees.models.job import Job
from src.modules.employees.models.work_history import WorkHistory
from src.modules.employees.schemas.employee_models import CreateEmployee
from src.modules.employees.services import sector_service
from sqlalchemy.orm import selectinload


def get_single_work_history_by_id(
    db: DatabaseSession, employee_id: int, work_history_id: int
) -> WorkHistory:
    result = db.exec(
        select(WorkHistory)
        .where(WorkHistory.id == work_history_id)
        .where(WorkHistory.employee_id == employee_id)
    ).one_or_none()

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"La work history con ID {work_history_id} del empleado {employee_id} no existe."
        )

    return result


def get_documents_of_employee(
    db: DatabaseSession,
    employee_id: int,
) -> Sequence[Document]:
    return db.exec(select(Document).where(Document.employee_id == employee_id)).all()


def get_document(db: DatabaseSession, document_id: int, employee_id: int) -> Document:
    result = db.exec(
        select(Document)
        .where(Document.id == document_id)
        .where(Document.employee_id == employee_id)
    ).one_or_none()

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"El documento con ID {document_id} del empleado con ID {employee_id} no existe."
        )

    return result


def count_active_employees(db: DatabaseSession) -> int:
    result = db.exec(select(func.count()).select_from(Employee).where(Employee.active))
    return result.one()


def get_employee_by_id(db: DatabaseSession, employee_id: int) -> Employee:
    """
    Obtiene un empleado por su ID, incluyendo sus relaciones.
    """
    stmt = (
        select(Employee)
        .where(Employee.id == employee_id)
        .options(
            selectinload(cast(Any, Employee.job)).selectinload(cast(Any, Job.sector)),
            selectinload(cast(Any, Employee.state)),
            selectinload(cast(Any, Employee.country)),
            selectinload(cast(Any, Employee.work_histories)),
            selectinload(cast(Any, Employee.documents)),
            selectinload(cast(Any, Employee.shift))
        )
    )

    result = db.exec(stmt).one_or_none()
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"El empleado con ID {employee_id} no existe."
        )
    return result



def get_employee_by_id_simple(db: DatabaseSession, employee_id: int) -> Employee:
    employee = db.exec(
        select(Employee).where(Employee.id == employee_id)
    ).one_or_none()

    if employee is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"El empleado con ID {employee_id} no existe."
        )

    return employee


def get_employee_by_user_id(db: DatabaseSession, user_id: str) -> Employee:
    employee = db.exec(
        select(Employee).where(Employee.user_id == user_id)
    ).one_or_none()

    if employee is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"El empleado con user_id {user_id} no existe."
        )

    return employee


def get_all_employees(db: DatabaseSession, sector_id: Optional[int]) -> Sequence[Employee]:
    stmt = select(Employee).order_by(cast(Any, Employee.id))
    if sector_id is not None:
        # Para dar error si no existe el sector
        sector_service.get_sector_by_id(db, sector_id)

        stmt = stmt.join(
            Job, cast(Any, Employee.job_id == Job.id)
        ).where(Job.sector_id == sector_id)
    return db.exec(stmt).all()


def create_user_id(db: DatabaseSession, employee_request: CreateEmployee) -> str:
    first_char = employee_request.first_name[0].lower()
    last_name = employee_request.last_name.lower()
    dni_suffix = employee_request.dni[-3:]

    base_user_id = f"{first_char}{last_name}{dni_suffix}"
    candidate_user_id = base_user_id
    counter = 0

    while db.exec(select(Employee).where(Employee.user_id == candidate_user_id)).one_or_none():
        counter += 1
        # Asegura que los últimos 3 sean siempre numéricos y con 3 cifras
        new_suffix = f"{int(dni_suffix) + counter:03d}"
        candidate_user_id = f"{first_char}{last_name}{new_suffix}"

    return candidate_user_id
