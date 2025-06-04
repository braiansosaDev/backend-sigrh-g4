from typing import List
from fastapi import HTTPException, status
from src.database.core import DatabaseSession
from src.modules.employees.models.work_history import WorkHistory
from src.modules.employees.schemas.work_history_models import WorkHistoryRequest
import src.modules.employees.services.utils as utils


def get_work_history(db: DatabaseSession, employee_id: int) -> List[WorkHistory]:
    employee = utils.get_employee_by_id(db, employee_id)
    work_histories = employee.work_histories

    if employee is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found."
        )
    return work_histories


def create_work_history(
    db: DatabaseSession, employee_id: int, work_history: WorkHistoryRequest
) -> WorkHistory:
    employee = utils.get_employee_by_id(db, employee_id)
    if employee is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee_id not found.",
        )
    history = WorkHistory(
        employee_id=employee_id,
        job_id=work_history.job_id,
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
    work_history_id: int,
    work_history_changes: WorkHistoryRequest,
) -> WorkHistory:
    employee = utils.get_employee_by_id(db, employee_id)
    register = utils.get_single_work_history_by_id(db, employee_id, work_history_id)

    if register is None or employee is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Work history_id or employee_id not found.",
        )
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
    employee = utils.get_employee_by_id(db, employee_id)
    register = utils.get_single_work_history_by_id(db, employee_id, work_history_id)

    if register is None or employee is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Work history_id or employee_id not found.",
        )
    db.delete(register)
    db.commit()
