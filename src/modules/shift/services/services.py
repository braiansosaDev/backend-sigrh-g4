from typing import Sequence
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlmodel import select
from src.database.core import DatabaseSession
from src.modules.shift.schemas.schemas import ShiftRequest
from src.modules.shift.models.models import Shift
import logging


def get_shift_by_id(db: DatabaseSession, id: int) -> Shift:
    shift = db.exec(select(Shift).where(Shift.id == id)).first()
    if not shift:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shift id was not found",
        )
    return shift


def get_shifts(db: DatabaseSession) -> Sequence[Shift]:
    return db.exec(select(Shift)).all()


def post_shift(db: DatabaseSession, request: ShiftRequest) -> Shift:
    try:
        db_shift = Shift(**request.model_dump())
        db.add(db_shift)
        db.commit()
        db.refresh(db_shift)
        return db_shift
    except IntegrityError as e:
        db.rollback()
        logging.error(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An unexpected error occurred",
        )


def patch_shift(db: DatabaseSession, shift_id: int, request: ShiftRequest) -> Shift:
    try:
        db_shift = get_shift_by_id(db, shift_id)
        if not db_shift:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Shift not found"
            )
        for attr, value in request.model_dump(exclude_unset=True).items():
            if hasattr(db_shift, attr):
                setattr(db_shift, attr, value)
        db.add(db_shift)
        db.commit()
        return db_shift
    except IntegrityError as e:
        db.rollback()
        logging.error(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An unexpected error occurred",
        )


def delete_shift(db: DatabaseSession, shift_id: int):
    try:
        db_shift = get_shift_by_id(db, shift_id)
        if not db_shift:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Shift not found"
            )
        db.delete(db_shift)
        db.commit()
    except IntegrityError as e:
        db.rollback()
        logging.error(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An unexpected error occurred",
        )
