from fastapi import APIRouter, status
from typing import List
from src.database.core import DatabaseSession
from src.modules.employees.schemas.state_models import StateResponse, CreateState, UpdateState
from src.modules.employees.services import state_service

state_router = APIRouter(prefix="/states", tags=["States"])

"""Enpoint para buscar una provincia por su ID. 
Returns:
    StateResponse: Devuelve los datos de la provincia.
"""

@state_router.get("/", response_model=List[StateResponse], status_code=status.HTTP_200_OK)
async def get_all_states(db: DatabaseSession):
    return state_service.get_all_states(db)

@state_router.get("/{state_id}", response_model=StateResponse, status_code=status.HTTP_200_OK)
async def get_state_by_id(db: DatabaseSession, state_id: int):    
    return state_service.get_state_by_id(db, state_id)

"""Enpoint para crear una provincia nueva.
Returns:
    StateResponse: Devuelve los datos de la provincia creada.
"""
@state_router.post("/create", response_model=StateResponse, status_code=status.HTTP_201_CREATED)
async def create_state(db: DatabaseSession, create_state_request: CreateState):
    return state_service.create_state(db, create_state_request)

"""Endpoint para actualizar los datos de una provincia.
Returns:
    StateResponse: Devuelve los datos de la provincia actualizada.
"""
@state_router.patch("/{state_id}", response_model=StateResponse, status_code=status.HTTP_200_OK)
async def update_state(state_id: int, update: UpdateState, db: DatabaseSession):
    return state_service.update_state(db,state_id, update)

"""Endpoint para eliminar una provincia.
Returns:
    CODE: 204
"""
@state_router.delete("/{state_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_state(state_id: int, db: DatabaseSession):
    return state_service.delete_state(db, state_id)

