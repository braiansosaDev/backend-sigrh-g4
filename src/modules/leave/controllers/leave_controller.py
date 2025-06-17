from fastapi import APIRouter, status, Query
from typing import Annotated
from src.database.core import DatabaseSession
from src.modules.auth.token import TokenDependency
from src.modules.leave.schemas.leave_schemas import (
    GetRequest,
    LeavePublic,
    LeaveCreate,
    LeaveUpdate,
    LeaveTypePublic,
    ReportRequest,
    ReportResponse,
)
from src.modules.leave.services import leave_service

leave_router = APIRouter(prefix="/leaves", tags=["Leaves"])


@leave_router.get("/", response_model=list[LeavePublic], status_code=status.HTTP_200_OK)
async def get_leaves(
    session: DatabaseSession,
    request: Annotated[GetRequest, Query()],
):
    return leave_service.get_leaves(
        session, request
    )


@leave_router.get(
    "/report", response_model=ReportResponse, status_code=status.HTTP_200_OK
)
async def get_report(
    session: DatabaseSession,
    token: TokenDependency,
    request: Annotated[ReportRequest, Query()],
):
    return leave_service.report(session, token, request)


@leave_router.get(
    "/types", response_model=list[LeaveTypePublic], status_code=status.HTTP_200_OK
)
async def get_leave_types(session: DatabaseSession):
    return leave_service.get_leave_types(session)


@leave_router.get(
    "/types/{leave_type_id}",
    response_model=LeaveTypePublic,
    status_code=status.HTTP_200_OK,
)
async def get_leave_type(session: DatabaseSession, leave_type_id: int):
    return leave_service.get_leave_type(session, leave_type_id)


@leave_router.get(
    "/{leave_id}", response_model=LeavePublic, status_code=status.HTTP_200_OK
)
async def get_leave(session: DatabaseSession, leave_id: int):
    return leave_service.get_leave(session, leave_id)


@leave_router.put("/", response_model=LeavePublic, status_code=status.HTTP_201_CREATED)
async def create_leave(
    session: DatabaseSession, token: TokenDependency, request: LeaveCreate
):
    return leave_service.create_leave(session, token, request)


@leave_router.patch(
    "/{leave_id}", response_model=LeavePublic, status_code=status.HTTP_200_OK
)
async def update_leave(
    session: DatabaseSession,
    token: TokenDependency,
    leave_id: int,
    request: LeaveUpdate,
):
    return leave_service.update_leave(session, token, leave_id, request)
