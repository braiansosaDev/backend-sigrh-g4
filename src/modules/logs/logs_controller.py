from . import log_schemas, log_service
from fastapi import APIRouter, Query, status
from src.database.core import DatabaseSession

logs_router = APIRouter(prefix="/logs", tags=["Logs"])


@logs_router.get(
    path="/",
    status_code=status.HTTP_200_OK,
    response_model=list[log_schemas.LogResponse],
)
async def list_logs(
    db: DatabaseSession,
    entity: str | None = Query(default=None, regex="^(LICENCIA|NOMINA|CONVOCATORIA)$"),
    entity_id: int | None = Query(default=None),
):
    return log_service.list_logs(db, entity, entity_id)


@logs_router.get(
    path="/{log_id}",
    status_code=status.HTTP_200_OK,
    response_model=log_schemas.LogResponse,
)
async def get_log(db: DatabaseSession, log_id: int):
    return log_service.get_log(db, log_id)


@logs_router.post(
    path="/",
    status_code=status.HTTP_201_CREATED,
    response_model=log_schemas.LogResponse,
)
async def create_log(db: DatabaseSession, request: log_schemas.LogCreateRequest):
    return log_service.create_log(db, request)


@logs_router.patch(
    path="/{log_id}",
    status_code=status.HTTP_200_OK,
    response_model=log_schemas.LogResponse,
)
async def update_log(
    db: DatabaseSession, request: log_schemas.LogUpdateRequest, log_id: int
):
    return log_service.update_log(db, request, log_id)


@logs_router.delete(path="/{log_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_logs(db: DatabaseSession, log_id: int):
    return log_service.delete_log(db, log_id)
