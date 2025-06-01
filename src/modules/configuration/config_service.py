from .config_models import Configuration
from .config_schemas import ConfigRequest
from src.database.core import DatabaseSession
from sqlmodel import select
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
import logging


def get_all_configurations(db: DatabaseSession):
    return db.exec(select(Configuration)).all()


def get_configurations(db: DatabaseSession, config_id: int):
    config = get_configurtation_by_id(db, config_id)
    if not config:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"La configuración con id {config_id} no fue encontrada",
        )
    return config


def get_configurtation_by_id(db: DatabaseSession, config_id: int):
    return db.exec(select(Configuration).where(Configuration.id == config_id)).first()


def create_configurations(db: DatabaseSession, request: ConfigRequest):
    try:
        config_db = Configuration(**request.model_dump())
        db.add(config_db)
        db.commit()
        db.refresh(config_db)
        return config_db
    except IntegrityError as e:
        db.rollback()
        logging.error(e.orig)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An unexpected error occurred",
        )


def update_configurations(db: DatabaseSession, config_id: int, request: ConfigRequest):
    try:
        config_db = get_configurtation_by_id(db, config_id)
        if not config_db:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"La configuración con id {config_id} no existe",
            )
        for attr, value in request.model_dump(exclude_unset=True).items():
            if hasattr(config_db, attr):
                setattr(config_db, attr, value)
        db.add(config_db)
        db.commit()
        return config_db
    except IntegrityError as e:
        db.rollback()
        logging.error(e.orig)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An unexpected error occurred",
        )


def delete_configurations(db: DatabaseSession, config_id: int):
    try:
        config_db = get_configurtation_by_id(db, config_id)
        if not config_db:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"La configuración con id {config_id} no existe",
            )
        db.delete(config_db)
        db.commit()
    except IntegrityError as e:
        db.rollback()
        logging.error(e.orig)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An unexpected error occurred",
        )
