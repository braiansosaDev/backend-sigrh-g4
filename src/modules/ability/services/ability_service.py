from src.database.core import DatabaseSession
from src.modules.ability.models.ability_models import Ability, AbilityBase
from sqlmodel import select
from typing import Sequence
from enum import Enum
from sqlalchemy.exc import IntegrityError
import logging


logger = logging.getLogger("uvicorn.error")


class ErrorCode(Enum):
    NOT_FOUND = "not_found"
    INTERNAL_ERROR = "internal_error"
    BAD_REQUEST = "bad_request"


def get_ability_by_id(
    db: DatabaseSession, ability_id: int
) -> Ability | tuple[ErrorCode, str]:
    result = db.exec(select(Ability).where(Ability.id == ability_id)).one_or_none()
    if result is None:
        return (ErrorCode.NOT_FOUND, f"The ability with id {ability_id} was not found.")
    else:
        return result


def get_all_abilities(db: DatabaseSession) -> Sequence[Ability]:
    return db.exec(select(Ability)).all()


def create_ability(
    db: DatabaseSession, request: AbilityBase
) -> Ability | tuple[ErrorCode, str]:
    try:
        db_ability = Ability(**request.dict())

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
