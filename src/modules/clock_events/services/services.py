from datetime import date, datetime
from typing import Optional, Sequence
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlmodel import select, text
from src.database.core import DatabaseSession
from src.modules.clock_events.schemas.schemas import ClockEventRequest
from src.modules.clock_events.models.models import ClockEvents
from src.modules.employees.models.employee import Employee
from src.modules.employees.models.job import Job
from src.modules.employees.services.utils import get_employee_by_id
import logging
from sqlalchemy.orm import selectinload

def get_attendance_resume(db: DatabaseSession, fecha: date):
    return get_clock_event_summary_by_date_sql(db, fecha)

def get_clock_event_summary_by_date_sql(db: DatabaseSession, fecha: date):
    query = text("""
        SELECT
            e.id AS employee_id,
            e.first_name,
            e.last_name,
            j.name AS job,
            :fecha AS date,
            MIN(CASE WHEN c.event_type = 'IN' THEN c.event_date END) AS first_in,
            MAX(CASE WHEN c.event_type = 'OUT' THEN c.event_date END) AS last_out,
            COUNT(c.id) AS total_events
        FROM employee e
        LEFT JOIN job j ON e.job_id = j.id
        LEFT JOIN clock_events c ON e.id = c.employee_id AND DATE(c.event_date) = :fecha
        WHERE e.active = TRUE
        GROUP BY e.id, e.first_name, e.last_name, j.name
        ORDER BY e.id
    """)

    result = db.execute(query, {"fecha": fecha})
    return [dict(row._mapping) for row in result]


def get_clock_event_by_id(db: DatabaseSession, id: int) -> ClockEvents | None:
    return db.exec(select(ClockEvents).where(ClockEvents.id == id)).first()

def get_clock_events(
    db: DatabaseSession,
    employee_id: Optional[int] = None,
    fecha: Optional[date] = None
) -> Sequence[ClockEvents]:
    stmt = select(ClockEvents)

    if employee_id:
        stmt = stmt.where(ClockEvents.employee_id == employee_id)

    if fecha:
        stmt = stmt.where(
            ClockEvents.event_date.between(
                datetime.combine(fecha, datetime.min.time()),
                datetime.combine(fecha, datetime.max.time())
            )
        )

    return db.exec(stmt.order_by(ClockEvents.event_date)).all()

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
