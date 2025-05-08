from fastapi import APIRouter

from src.database.core import DatabaseSession
from src.modules.ability.models.ability_models import AbilityModel
from src.modules.ability.schemas.ability_schemas import AbilityPublic, AbilityRequest
from src.modules.ability.services import ability_service
from src.modules.ability.services.ability_service import ErrorCode
from typing import Sequence, Any
from fastapi import status, HTTPException
import logging


logger = logging.getLogger("uvicorn.error")

error_dict: dict[ErrorCode, int] = {}
error_dict[ErrorCode.NOT_FOUND] = status.HTTP_404_NOT_FOUND
error_dict[ErrorCode.INTERNAL_ERROR] = status.HTTP_500_INTERNAL_SERVER_ERROR
error_dict[ErrorCode.BAD_REQUEST] = status.HTTP_400_BAD_REQUEST


def get_http_status_code(error_code: ErrorCode) -> int:
    if error_code in error_dict:
        return error_dict[error_code]
    else:
        logger.error(
            f"Tried to use error code {error_code} not mapped to any status code"
        )
        raise ValueError()


def log_unknown_response(module_name: str, service_response: Any) -> None:
    logging.error(
        f"{module_name}: Unknown response type from service: {type(service_response)}"
    )
    logging.error(f"Reponse data: {service_response}")
    raise ValueError("Unkown response type from service")


ability_router = APIRouter(prefix="/abilities", tags=["Abilities"])


@ability_router.get("/", response_model=list[AbilityPublic])
async def get_all_abilities(db: DatabaseSession) -> Sequence[AbilityModel]:
    return ability_service.get_all_abilities(db)


@ability_router.get("/{ability_id}", response_model=AbilityPublic)
async def get_ability_by_id(db: DatabaseSession, ability_id: int) -> AbilityModel:
    service_response = ability_service.get_ability_by_id(db, ability_id)

    match service_response:
        case AbilityModel():
            return service_response
        case (ErrorCode(), str()):
            raise HTTPException(
                status_code=get_http_status_code(service_response[0]),
                detail=service_response[1],
            )
        case _:
            log_unknown_response(__name__, service_response)


@ability_router.post(
    "/create", status_code=status.HTTP_201_CREATED, response_model=AbilityPublic
)
async def create_ability(db: DatabaseSession, body: AbilityRequest):
    service_response = ability_service.create_ability(db, body)

    match service_response:
        case AbilityModel():
            return service_response
        case (ErrorCode(), str()):
            raise HTTPException(
                status_code=get_http_status_code(service_response[0]),
                detail=service_response[1],
            )
        case _:
            log_unknown_response(__name__, service_response)
