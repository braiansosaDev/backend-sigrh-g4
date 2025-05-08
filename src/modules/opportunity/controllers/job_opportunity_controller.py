from fastapi import APIRouter, status
from src.database.core import DatabaseSession
from src.modules.opportunity.schemas.job_opportunity_schemas import (
    JobOpportunityResponse,
    JobOpportunityRequest,
    JobOpportunityUpdate
)
from src.modules.opportunity.services import opportunity_service


opportunity_router = APIRouter(prefix="/opportunities", tags=["Opportunities"])


@opportunity_router.get(
    "/", status_code=status.HTTP_200_OK, response_model=list[JobOpportunityResponse]
)
async def get_all_opportunities_with_abilities(db: DatabaseSession):
    return opportunity_service.get_all_opportunities_with_abilities(db)


@opportunity_router.get(
    "/{opportunity_id}",
    status_code=status.HTTP_200_OK,
    response_model=JobOpportunityResponse,
)
async def get_opportunity_with_abilities(db: DatabaseSession, opportunity_id: int):
    return opportunity_service.get_opportunity_with_abilities(db, opportunity_id)


@opportunity_router.post(
    "/create",
    status_code=status.HTTP_201_CREATED,
    response_model=JobOpportunityResponse,
)
async def create_opportunity(
    db: DatabaseSession, job_opportunity_request: JobOpportunityRequest
):
    return opportunity_service.create_opportunity(db, job_opportunity_request)

@opportunity_router.patch("/{opportunity_id}", status_code=status.HTTP_200_OK, response_model=JobOpportunityResponse)
async def update_opportunity(db: DatabaseSession, opportunity_id: int, patch: JobOpportunityUpdate):
    return opportunity_service.update_opportunity(db, opportunity_id, patch)


@opportunity_router.delete("/{opportunity_id}", status_code=status.HTTP_200_OK)
async def delete_opportunity(db: DatabaseSession, opportunity_id: int) -> None:
    return opportunity_service.delete_opportunity(db, opportunity_id)
