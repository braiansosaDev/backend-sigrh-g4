from src.database.core import DatabaseSession
from src.modules.ability.models.ability_models import AbilityModel
from sqlmodel import select
from typing import Sequence
from enum import Enum
from sqlalchemy.exc import IntegrityError
import logging

from src.modules.ability.schemas.ability_schemas import AbilityRequest


logger = logging.getLogger("uvicorn.error")


class ErrorCode(Enum):
    NOT_FOUND = "not_found"
    INTERNAL_ERROR = "internal_error"
    BAD_REQUEST = "bad_request"


def get_ability_by_id(
    db: DatabaseSession, ability_id: int
) -> AbilityModel | tuple[ErrorCode, str]:
    result = db.exec(select(AbilityModel).where(AbilityModel.id == ability_id)).one_or_none()
    if result is None:
        return (ErrorCode.NOT_FOUND, f"The ability with id {ability_id} was not found.")
    else:
        return result


def get_all_abilities(db: DatabaseSession) -> Sequence[AbilityModel]:
    return db.exec(select(AbilityModel)).all()


def create_ability(
    db: DatabaseSession, request: AbilityRequest
) -> AbilityModel | tuple[ErrorCode, str]:
    try:
        db_ability = AbilityModel(**request.dict())

        db.add(db_ability)
        db.commit()
        return db_ability
    except IntegrityError as e:
        db.rollback()
        if 'duplicate key value violates unique constraint "ix_ability_name"' in str(
            e.orig
        ):
            return (
                ErrorCode.BAD_REQUEST,
                f"The ability with name {request.name} already exists.",
            )
        else:
            logger.error(e.orig)
            return (ErrorCode.INTERNAL_ERROR, "Unknown internal error")
