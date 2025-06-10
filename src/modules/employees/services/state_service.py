from src.database.core import DatabaseSession
from src.modules.employees.schemas.state_models import CreateState, UpdateState
from src.modules.employees.models.state import State
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlmodel import select
from typing import cast, Any
import logging

logger = logging.getLogger("uvicorn.error")

def get_all_states(db: DatabaseSession):
    return db.exec(
        select(State)
        .order_by(cast(Any, State.id))
    ).all()

def get_state_by_id_or_none(db: DatabaseSession, state_id: int) -> State | None:
    return db.exec(select(State).where(State.id == state_id)).one_or_none()

def get_state_by_id(db: DatabaseSession, state_id: int) -> State:
    result = get_state_by_id_or_none(db, state_id)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"State with ID {state_id} not found."
        )
    return result

def create_state(db: DatabaseSession,create_state_request: CreateState,) -> State:
    db_state = State(
        name=create_state_request.name,
        country_id=create_state_request.country_id
    )
    db.add(db_state)
    db.commit()
    db.refresh(db_state)
    return db_state


def update_state(db: DatabaseSession, state_id: int, update_state_request: UpdateState) -> State:
    state = get_state_by_id(db, state_id)

    if update_state_request.name is not None:
        state.name = update_state_request.name
    if update_state_request.country_id is not None:
        state.country_id = update_state_request.country_id

    try:
        db.add(state)
        db.commit()
        db.refresh(state)
        return state
    except IntegrityError:
        db.rollback()
        logger.error(f"An unexpected IntegrityError occurred while updating State with ID {state_id} and data {update_state_request.model_dump_json()}")
        raise


def delete_state(db: DatabaseSession, state_id: int) -> None:
    db_state = get_state_by_id(db, state_id)

    try:
        db.delete(db_state)
        db.commit()
    except IntegrityError:
        db.rollback()
        logger.error(f"An unexpected IntegrityError occurred while deleting State with ID {state_id}")
        raise
