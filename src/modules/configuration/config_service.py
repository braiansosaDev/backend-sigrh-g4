from .config_models import Configuration
from .config_schemas import ConfigRequest
from src.database.core import DatabaseSession
from sqlmodel import select
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
import logging

def get_configurations(db: DatabaseSession):
    config = get_configuration_by_id(db, 1)
    if not config:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se encontró la configuración del sistema",
        )
    return config

def get_configuration_by_id(db: DatabaseSession, config_id: int):
    return db.exec(select(Configuration).where(Configuration.id == config_id)).first()


def set_configurations(db: DatabaseSession, request: ConfigRequest):
    try:
        # Siempre trabajamos con ID fijo = 1
        existing_config = get_configuration_by_id(db, 1)

        if existing_config:
            # Actualizar los campos si ya existe
            for attr, value in request.model_dump().items():
                if hasattr(existing_config, attr):
                    setattr(existing_config, attr, value)
            db.add(existing_config)
            db.commit()
            db.refresh(existing_config)
            return existing_config
        else:
            # Crear nueva configuración con ID 1
            config_db = Configuration(id=1, **request.model_dump())
            db.add(config_db)
            db.commit()
            db.refresh(config_db)
            return config_db

    except IntegrityError as e:
        db.rollback()
        logging.error(e.orig)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ocurrió un error inesperado al guardar la configuración",
        )


def update_configurations(db: DatabaseSession, config_id: int, request: ConfigRequest):
    try:
        config_db = get_configuration_by_id(db, config_id)
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
        config_db = get_configuration_by_id(db, config_id)
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
