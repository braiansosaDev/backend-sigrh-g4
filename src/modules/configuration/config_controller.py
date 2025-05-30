from fastapi import APIRouter, status
from . import config_schemas, config_service
from src.database.core import DatabaseSession

config_router = APIRouter(prefix="/configurations", tags=["Configurations"])


@config_router.get(
    path="/",
    response_model=list[config_schemas.ConfigResponse],
    status_code=status.HTTP_200_OK,
)
async def get_all_configurations(db: DatabaseSession):
    return config_service.get_all_configurations(db)


@config_router.get(
    path="/{id}",
    response_model=config_schemas.ConfigResponse,
    status_code=status.HTTP_200_OK,
)
async def get_configurations(db: DatabaseSession, id: int):
    return config_service.get_configurations(db, id)


@config_router.post(
    path="/",
    response_model=config_schemas.ConfigResponse,
    status_code=status.HTTP_201_CREATED,
)
async def post_configurations(
    db: DatabaseSession, request: config_schemas.ConfigRequest
):
    return config_service.create_configurations(db, request)


@config_router.patch(
    path="/{id}",
    response_model=config_schemas.ConfigResponse,
    status_code=status.HTTP_200_OK,
)
async def patch_configurations(
    db: DatabaseSession, id: int, request: config_schemas.ConfigRequest
):
    return config_service.update_configurations(db, id, request)


@config_router.delete(path="/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_configurations(db: DatabaseSession, id: int):
    return config_service.delete_configurations(db, id)
