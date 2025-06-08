from typing import Sequence
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlmodel import select
from src.database.core import DatabaseSession
from src.modules.concept.models.models import Concept
from src.modules.employee_hours.schemas.schemas import EmployeeHoursRequest, EmployeeHoursPatchRequest
from src.modules.employee_hours.models.models import EmployeeHours
from src.modules.employees.models.employee import Employee
from src.modules.employees.services.utils import get_employee_by_id
from src.modules.concept.services.service import get_concept_by_id
from src.modules.shift.models.models import Shift
from src.modules.shift.services.services import get_shift_by_id
import logging


def get_employee_hours_by_id(db: DatabaseSession, id: int) -> EmployeeHours:
    employee_hours = db.exec(
        select(EmployeeHours).where(EmployeeHours.id == id)
    ).first()
    if not employee_hours:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee hours id was not found",
        )
    return employee_hours


def get_all_employee_hours(db: DatabaseSession) -> Sequence[EmployeeHours]:
    return db.exec(select(EmployeeHours)).all()


def post_employee_hours(
    db: DatabaseSession, request: EmployeeHoursRequest
) -> EmployeeHours:
    try:
        employee = get_employee_by_id(db, request.employee_id)
        concept = get_concept_by_id(db, request.concept_id)
        shift = get_shift_by_id(db, request.shift_id)

        if not employee:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found"
            )
        if not concept:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Concept not found"
            )
        if not shift:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Shift not found"
            )
        db_employee_hours = EmployeeHours(**request.model_dump())
        db.add(db_employee_hours)
        db.commit()
        db.refresh(db_employee_hours)
        return db_employee_hours
    except IntegrityError as e:
        db.rollback()
        logging.error(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An unexpected error occurred",
        )


def patch_employee_hours(
    db: DatabaseSession, employee_hours_id: int, request: EmployeeHoursPatchRequest
) -> EmployeeHours:
    try:
        # employee = get_employee_by_id(db, request.employee_id)
        # concept = get_concept_by_id(db, request.concept_id)
        # shift = get_shift_by_id(db, request.shift_id)
        db_employee_hours = get_employee_hours_by_id(db, employee_hours_id)

        # validate_employee_hours(employee, concept, shift, db_employee_hours)

        for attr, value in request.model_dump(exclude_unset=True).items():
            if hasattr(db_employee_hours, attr):
                setattr(db_employee_hours, attr, value)
        db.add(db_employee_hours)
        db.commit()
        return db_employee_hours
    except IntegrityError as e:
        db.rollback()
        logging.error(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An unexpected error occurred",
        )


def delete_employee_hours(db: DatabaseSession, employee_hours_id: int):
    try:
        db_employee_hours = get_employee_hours_by_id(db, employee_hours_id)
        if not db_employee_hours:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Employee hours was not found",
            )
        db.delete(db_employee_hours)
        db.commit()
    except IntegrityError as e:
        db.rollback()
        logging.error(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An unexpected error occurred",
        )


def validate_employee_hours(
    employee: Employee, concept: Concept, shift: Shift, db_employee_hours: EmployeeHours
):
    if db_employee_hours.employee_id != employee.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Employee id doesn't match"
        )
    if db_employee_hours.concept_id != concept.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Concept id doesn't match"
        )
    if db_employee_hours.shift_id != shift.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Shift id doesn't match"
        )
