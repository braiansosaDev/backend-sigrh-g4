from fastapi import APIRouter

from src.database.core import DatabaseSession
from src.modules.ability.models.ability_models import AbilityModel
from src.modules.ability.schemas.ability_schemas import AbilityPublic, AbilityRequest, AbilityUpdate
from src.modules.ability.services import ability_service
from typing import Sequence
from fastapi import status
import logging


logger = logging.getLogger("uvicorn.error")
ability_router = APIRouter(prefix="/abilities", tags=["Abilities"])


@ability_router.get("/", response_model=list[AbilityPublic])
async def get_all_abilities(db: DatabaseSession) -> Sequence[AbilityModel]:
    return ability_service.get_all_abilities(db)


@ability_router.get("/{ability_id}", response_model=AbilityPublic)
async def get_ability_by_id(db: DatabaseSession, ability_id: int) -> AbilityModel:
    return ability_service.get_ability_by_id(db, ability_id)


@ability_router.post(
    "/create", status_code=status.HTTP_201_CREATED, response_model=AbilityPublic
)
async def create_ability(db: DatabaseSession, body: AbilityRequest):
    return ability_service.create_ability(db, body)


@ability_router.patch("/{ability_id}", status_code=status.HTTP_200_OK, response_model=AbilityPublic)
async def update_ability(db: DatabaseSession, ability_id: int, body: AbilityUpdate):
    return ability_service.update_ability(db, ability_id, body)


@ability_router.delete("/{ability_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_ability(db: DatabaseSession, ability_id: int) -> None:
    return ability_service.delete_ability(db, ability_id)
