from src.database.core import DatabaseSession
from src.modules.ability.models.ability_models import AbilityModel
from sqlmodel import select
from typing import Sequence
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
import logging

from src.modules.ability.schemas.ability_schemas import AbilityRequest, AbilityUpdate


logger = logging.getLogger("uvicorn.error")


def get_ability_by_id(
    db: DatabaseSession, ability_id: int
) -> AbilityModel:
    result = db.exec(select(AbilityModel).where(AbilityModel.id == ability_id)).one_or_none()
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The ability with id {ability_id} does not exist.")
    return result

def get_ability_by_name(db: DatabaseSession, ability_name: str) -> AbilityModel:
    result = db.exec(select(AbilityModel).where(AbilityModel.name == ability_name)).one_or_none()
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The ability with name {ability_name} does not exist.")
    return result

def get_all_abilities(db: DatabaseSession) -> Sequence[AbilityModel]:
    return db.exec(select(AbilityModel)).all()


def create_ability(
    db: DatabaseSession, request: AbilityRequest
) -> AbilityModel:
    try:
        db_ability = AbilityModel(**request.dict())

        db.add(db_ability)
        db.commit()
        return db_ability
    except IntegrityError as e:
        db.rollback()
        if 'duplicate key value violates unique constraint' in str(
            e.orig
        ):
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                detail=f"The ability with name {request.name} already exists.",
            )
        else:
            logger.error(e.orig)
            raise

def update_ability(db: DatabaseSession, ability_id: int, request: AbilityUpdate) -> AbilityModel:
    try:
        db_ability = get_ability_by_id(db, ability_id)
        for attr, value in request.model_dump(exclude_unset=True).items():
            if hasattr(db_ability, attr):
                setattr(db_ability, attr, value)

        db.add(db_ability)
        db.commit()
        return db_ability
    except IntegrityError as e:
        db.rollback()
        if 'duplicate key value violates unique constraint' in str(e.orig):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"The ability with name {request.name} already exists.")

        logger.error(f"Unexpected IntegrityError while udpating ability with id {ability_id} and data {request.model_dump_json()}")
        logger.error(e)
        raise

def delete_ability(db: DatabaseSession, ability_id: int) -> None:
    try:
        db_ability = get_ability_by_id(db, ability_id)
        db.delete(db_ability)
        db.commit()
    except IntegrityError as e:
        db.rollback()
        logger.error(f"Unexpected IntegrityError while deleting ability with id {ability_id}")
        logger.error(e)
        raise
