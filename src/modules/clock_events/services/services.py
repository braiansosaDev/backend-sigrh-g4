from typing import Sequence
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlmodel import select
from src.database.core import DatabaseSession
from src.modules.clock_events.schemas.schemas import ClockEventRequest
from src.modules.clock_events.models.models import ClockEvents
from src.modules.employees.services.utils import get_employee_by_id
import logging


def get_clock_event_by_id(db: DatabaseSession, id: int) -> ClockEvents | None:
    return db.exec(select(ClockEvents).where(ClockEvents.id == id)).first()


def get_clock_events(db: DatabaseSession) -> Sequence[ClockEvents]:
    return db.exec(select(ClockEvents)).all()


def post_clock_event(db: DatabaseSession, request: ClockEventRequest) -> ClockEvents:
    try:
        employee = get_employee_by_id(db, request.employee_id)
        if not employee:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found"
            )
        db_clock_event = ClockEvents(**request.model_dump())
        db.add(db_clock_event)
        db.commit()
        db.refresh(db_clock_event)
        return db_clock_event
    except IntegrityError as e:
        db.rollback()
        logging.error(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An unexpected error occurred",
        )


def patch_clock_event(
    db: DatabaseSession, clock_event_id: int, request: ClockEventRequest
) -> ClockEvents:
    try:
        employee = get_employee_by_id(db, request.employee_id)
        if not employee:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found"
            )
        db_clock_event = get_clock_event_by_id(db, clock_event_id)
        if not db_clock_event:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Clock event not found"
            )
        if employee.id != db_clock_event.employee_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Employee id provided doesn't match",
            )
        for attr, value in request.model_dump(exclude_unset=True).items():
            if hasattr(db_clock_event, attr):
                setattr(db_clock_event, attr, value)
        db.add(db_clock_event)
        db.commit()
        return db_clock_event
    except IntegrityError as e:
        db.rollback()
        logging.error(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An unexpected error occurred",
        )


def delete_clock_event(db: DatabaseSession, clock_event_id: int):
    try:
        db_clock_event = get_clock_event_by_id(db, clock_event_id)
        if not db_clock_event:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Clock event not found"
            )
        db.delete(db_clock_event)
        db.commit()
    except IntegrityError as e:
        db.rollback()
        logging.error(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An unexpected error occurred",
        )
