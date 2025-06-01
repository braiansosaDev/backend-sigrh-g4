from fastapi import APIRouter, status
from . import config_schemas, config_service
from src.database.core import DatabaseSession

config_router = APIRouter(prefix="/configurations", tags=["Configurations"])


@config_router.post(
    path="/getConfigurations",
    response_model=config_schemas.ConfigBase,
    status_code=status.HTTP_200_OK,
)
async def get_configurations(db: DatabaseSession):
    return config_service.get_configurations(db)

#
# @config_router.get(
#     path="/{config_id}",
#     response_model=config_schemas.ConfigResponse,
#     status_code=status.HTTP_200_OK,
# )
# async def get_configurations_by_id(db: DatabaseSession, config_id: int):
#     return config_service.get_configuration_by_id(db, config_id)


@config_router.post(
    path="/setConfigurations",
    response_model=config_schemas.ConfigResponse,
    status_code=status.HTTP_201_CREATED,
)
async def post_configurations(
    db: DatabaseSession, request: config_schemas.ConfigRequest
):
    return config_service.set_configurations(db, request)


# @config_router.patch(
#     path="/{config_id}",
#     response_model=config_schemas.ConfigResponse,
#     status_code=status.HTTP_200_OK,
# )
# async def patch_configurations(
#     db: DatabaseSession, config_id: int, request: config_schemas.ConfigRequest
# ):
#     return config_service.update_configurations(db, config_id, request)


# @config_router.delete(path="/{config_id}", status_code=status.HTTP_204_NO_CONTENT)
# async def delete_configurations(db: DatabaseSession, config_id: int):
#     return config_service.delete_configurations(db, config_id)
