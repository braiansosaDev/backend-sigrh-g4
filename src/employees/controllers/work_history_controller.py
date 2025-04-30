from typing import List
from fastapi import APIRouter
from src.database.core import DatabaseSession
from src.auth.token import TokenDependency
from src.employees.services import work_history_service
from src.schemas.work_history_models import (
    WorkHistoryResponse,
    WorkHistoryRequest,
)

work_history_router = APIRouter(prefix="/work-history", tags=["Work History"])


@work_history_router.get(
    "/{employee_id}", status_code=200, response_model=List[WorkHistoryResponse]
)
async def get_work_history_of_employee(
    db: DatabaseSession,
    token: TokenDependency,
    employee_id: int,
):
    return work_history_service.get_work_history(db, employee_id)


@work_history_router.post(
    "/{employee_id}", status_code=201, response_model=WorkHistoryResponse
)
async def create_work_history_for_employee(
    db: DatabaseSession,
    token: TokenDependency,
    employee_id: int,
    work_history: WorkHistoryRequest,
):
    return work_history_service.create_work_history(db, employee_id, work_history)


@work_history_router.patch(
    "/{employee_id}/{work_history_id}",
    status_code=200,
    response_model=WorkHistoryResponse,
)
async def update_work_history_of_employee(
    db: DatabaseSession,
    token: TokenDependency,
    employee_id: int,
    work_history_id: int,
    changes: WorkHistoryRequest,
):
    return work_history_service.update_work_history_register(
        db, employee_id, work_history_id, changes
    )


@work_history_router.delete("/{employee_id}/{work_history_id}", status_code=204)
async def delete_work_history_of_employee(
    db: DatabaseSession, token: TokenDependency, employee_id: int, work_history_id: int
):
    return work_history_service.delete_work_history_register(
        db, employee_id, work_history_id
    )
