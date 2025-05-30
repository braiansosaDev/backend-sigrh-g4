from .config_models import Configuration
from .config_schemas import ConfigRequest
from src.database.core import DatabaseSession
from sqlmodel import select
from fastapi import HTTPException, status


def get_all_configurations(db: DatabaseSession):
    return db.exec(select(Configuration)).all()


def get_configurations(db: DatabaseSession, id: int):
    config = db.exec(select(Configuration).where(Configuration.id == id)).first()
    if not config:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"La configuración con id {id} no fue encontrada",
        )
    return config


def create_configurations(db: DatabaseSession, request: ConfigRequest):
    pass


def update_configurations(db: DatabaseSession, id: int, request: ConfigRequest):
    pass


def delete_configurations(db: DatabaseSession, id: int):
    pass
