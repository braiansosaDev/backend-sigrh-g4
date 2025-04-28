from typing import List
from sqlmodel import select
from src.database.core import DatabaseSession
from src.schemas.entities import WorkHistory
from src.schemas.work_history_models import WorkHistoryRequest


def get_single_work_history_by_id(
    db: DatabaseSession, employee_id: int, work_history_id: int
) -> WorkHistory:
    return db.exec(
        select(WorkHistory)
        .where(WorkHistory.id == work_history_id)
        .where(WorkHistory.employee_id == employee_id)
    ).first()


def get_work_history_of_employee(
    employee_id: int, db: DatabaseSession
) -> List[WorkHistory]:
    return db.exec(
        select(WorkHistory).where(WorkHistory.employee_id == employee_id)
    ).all()


def create_work_history(
    db: DatabaseSession, employee_id: int, work_history: WorkHistoryRequest
) -> WorkHistory:
    history = WorkHistory(
        employee_id=employee_id,
        job_title=work_history.job_title,
        from_date=work_history.from_date,
        to_date=work_history.to_date,
        company_name=work_history.company_name,
        notes=work_history.notes,
    )
    db.add(history)
    db.commit()
    db.refresh(history)
    return history


def update_work_history_register(
    db: DatabaseSession,
    employee_id: int,
    work_history_employee: int,
    work_history_changes: WorkHistoryRequest,
) -> WorkHistory:
    register = get_single_work_history_by_id(db, employee_id, work_history_employee)

    for attr, value in work_history_changes.model_dump(exclude_unset=True).items():
        if hasattr(register, attr):
            setattr(register, attr, value)

    db.add(register)
    db.commit()
    db.refresh(register)
    return register


def delete_work_history_register(
    db: DatabaseSession, employee_id: int, work_history_id: int
) -> None:
    register = get_single_work_history_by_id(db, employee_id, work_history_id)
    db.delete(register)
    db.commit()
