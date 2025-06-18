from . import log_model, log_schemas
from src.database.core import DatabaseSession
from fastapi import HTTPException, status
from sqlmodel import select
import logging
from datetime import datetime


def list_logs(db: DatabaseSession, entity: str | None, entity_id: int | None):
    query = select(log_model.Log)
    if entity:
        query = query.where(log_model.Log.entity == entity)
    if entity_id:
        query = query.where(log_model.Log.entity_id == entity_id)

    return db.exec(query).all()


def get_log(db: DatabaseSession, log_id: int):
    log = db.exec(select(log_model.Log).where(log_model.Log.id == log_id)).first()
    if not log:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found"
        )
    return log


def create_log(db: DatabaseSession, request: log_schemas.LogCreateRequest):
    try:
        log = log_model.Log(**request.model_dump())
        db.add(log)
        db.commit()
        db.refresh(log)
        return log
    except Exception as e:
        db.rollback()
        logging.error(e)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="An unexpected error occurred"
        )


def update_log(db: DatabaseSession, request: log_schemas.LogUpdateRequest, log_id: int):
    log = get_log(db, log_id)
    for attr, val in request.model_dump(exclude_unset=True).items():
        if hasattr(log, attr):
            setattr(log, attr, val)
    log.date_change = datetime.now()
    try:
        db.add(log)
        db.commit()
        return log
    except Exception as e:
        db.rollback()
        logging.error(e)
        raise HTTPException(
            status_code=status.HTTP_304_NOT_MODIFIED,
            detail="An unexpected error occurred",
        )


def delete_log(db: DatabaseSession, log_id: int):
    log = get_log(db, log_id)
    try:
        db.delete(log)
        db.commit()
    except Exception as e:
        db.rollback()
        logging.error(e)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="An unexpected error occurred"
        )
