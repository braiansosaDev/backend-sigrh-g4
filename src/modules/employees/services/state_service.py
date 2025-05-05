from src.database.core import DatabaseSession
from src.modules.employees.schemas.state_models import CreateState, UpdateState
from src.modules.employees.models.state import State
from fastapi import HTTPException, status
from sqlmodel import select

def get_all_states(db: DatabaseSession):
    return db.exec(select(State)).all()

def get_state_by_id(db: DatabaseSession, state_id: int) -> State:
    return db.exec(
        select(State)
        .where(State.id == state_id)
    ).one_or_none()

def create_state(db: DatabaseSession,create_state_request: CreateState,) -> State:
    db_state = State(
        name=create_state_request.name,
        country_id=create_state_request.country_id
    )
    db.add(db_state)
    db.commit()
    db.refresh(db_state)
    return db_state


def update_state(db: DatabaseSession,update_state_request: UpdateState, state_id: int) -> State:
    state = db.exec(
        select(State).where(State.id == state_id)
    ).one_or_none()

    if state is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="State not found."
        )

    state.name = update_state_request.name
    state.country_id = update_state_request.country_id
    db.add(state)
    db.commit()
    db.refresh(state)
    return state
    

def delete_state(db: DatabaseSession,state_id: int) -> None:
    state = db.exec(
        select(State).where(State.id == state_id)
    ).one_or_none()

    if state is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="State not found."
        )

    db.delete(state)
    db.commit()
