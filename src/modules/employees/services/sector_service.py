from src.database.core import DatabaseSession
from src.modules.employees.schemas.sector_models import CreateSector, UpdateSector
from src.modules.employees.models.sector import Sector
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlmodel import select
from typing import cast, Any
import logging

logger = logging.getLogger("uvicorn.error")


def get_all_sectors(db: DatabaseSession):
    return db.exec(
        select(Sector)
        .order_by(cast(Any, Sector.id))
    ).all()


def get_sector_by_id_or_none(db: DatabaseSession, sector_id: int) -> Sector | None:
    return db.exec(select(Sector).where(Sector.id == sector_id)).one_or_none()


def get_sector_by_id(db: DatabaseSession, sector_id: int) -> Sector:
    result = get_sector_by_id_or_none(db, sector_id)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"El Sector con ID {sector_id} no existe."
        )
    return result


def create_sector(db: DatabaseSession, create_sector_request: CreateSector) -> Sector:
    db_sector = Sector(name=create_sector_request.name)

    try:
        db.add(db_sector)
        db.commit()
        db.refresh(db_sector)
        return db_sector
    except IntegrityError:
        db.rollback()
        logger.error(f"An unexpected IntegrityError occurred while creating Sector with data {create_sector_request.model_dump_json()}")
        raise


def update_sector(db: DatabaseSession, sector_id: int, update_sector_request: UpdateSector) -> Sector:
    db_sector = get_sector_by_id(db, sector_id)

    for attr, value in update_sector_request.dict(exclude_unset=True).items():
        setattr(db_sector, attr, value)

    try:
        db.add(db_sector)
        db.commit()
        db.refresh(db_sector)
        return db_sector
    except IntegrityError:
        db.rollback()
        logger.error(f"An unexpected IntegrityError occurred while updating Sector with ID {sector_id} and data {update_sector_request.model_dump_json()}")
        raise


def delete_sector(db: DatabaseSession, sector_id: int) -> None:
    db_sector = get_sector_by_id(db, sector_id)

    try:
        db.delete(db_sector)
        db.commit()
    except IntegrityError:
        db.rollback()
        logger.error(f"An unexpected IntegrityError occurred while deleting sector with ID {sector_id}")
        raise
