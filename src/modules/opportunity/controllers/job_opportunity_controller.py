from datetime import date, datetime
from typing import Optional
from fastapi import APIRouter, Query, status
from src.database.core import DatabaseSession
from src.modules.opportunity.schemas.job_opportunity_schemas import (
    JobOpportunityActiveCountRequest,
    JobOpportunityActiveCountResponse,
    JobOpportunityAndPostulationsResponse,
    JobOpportunityResponse,
    JobOpportunityRequest,
    JobOpportunityStatus,
    JobOpportunityUpdate,
)
from src.modules.opportunity.services import opportunity_service
from src.modules.auth.token import TokenDependency
from src.modules.postulation.schemas.postulation_schemas import IndicatorsPostulationsResponse, RejectedPostulationsResponse


opportunity_router = APIRouter(prefix="/opportunities", tags=["Opportunities"])


@opportunity_router.post(
    "/active-count",
    status_code=status.HTTP_200_OK,
    summary="Cantidad de oportunidades activas",
)
async def count_active_opportunities(db: DatabaseSession):
    return {"active_count": opportunity_service.count_active_opportunities(db)}


@opportunity_router.get(
    "/", status_code=status.HTTP_200_OK, response_model=list[JobOpportunityResponse]
)
async def get_all_opportunities_with_abilities(
    db: DatabaseSession,
    status: Optional[JobOpportunityStatus] = Query(default=None),
    from_date: Optional[datetime] = Query(None, description="Fecha de inicio"),
    to_date: Optional[datetime] = Query(None, description="Fecha de fin"),
):
    return opportunity_service.get_all_opportunities_with_abilities(db, status, from_date, to_date)

@opportunity_router.get(
    "/opportunities-postulations", status_code=status.HTTP_200_OK, response_model=list[JobOpportunityAndPostulationsResponse]
)
async def get_all_opportunities_with_postulations(
    db: DatabaseSession,
    from_date: Optional[datetime] = Query(None, description="Fecha de inicio"),
    to_date: Optional[datetime] = Query(None, description="Fecha de fin"),
):
    return opportunity_service.get_all_opportunities_with_postulations(db, from_date, to_date)

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
    db: DatabaseSession,
    job_opportunity_request: JobOpportunityRequest,
    payload: TokenDependency,  # ⬅️ obtenemos el token decodificado
):
    employee_id = payload.get("employee_id")

    # Si tu modelo permite modificar el diccionario directamente
    job_opportunity_request_data = job_opportunity_request.dict()
    job_opportunity_request_data["owner_employee_id"] = employee_id

    return opportunity_service.create_opportunity(
        db, JobOpportunityRequest(**job_opportunity_request_data)
    )


@opportunity_router.patch(
    "/{opportunity_id}",
    status_code=status.HTTP_200_OK,
    response_model=JobOpportunityResponse,
)
async def update_opportunity(
    db: DatabaseSession, opportunity_id: int, patch: JobOpportunityUpdate
):
    return opportunity_service.update_opportunity(db, opportunity_id, patch)


@opportunity_router.delete("/{opportunity_id}", status_code=status.HTTP_200_OK)
async def delete_opportunity(db: DatabaseSession, opportunity_id: int) -> None:
    return opportunity_service.delete_opportunity(db, opportunity_id)


@opportunity_router.post(
    "/count-active-inactive",
    status_code=status.HTTP_200_OK,
    summary="Cantidad de oportunidades activas e inactivas",
    response_model=JobOpportunityActiveCountResponse,
)
async def get_active_opportunity_count(db: DatabaseSession, JobOpportunityActiveCountRequest: JobOpportunityActiveCountRequest):
    return opportunity_service.get_active_inactive_opportunity_count_by_date(db, JobOpportunityActiveCountRequest)


@opportunity_router.get(
    "/rejected-postulations-count/{opportunity_id}",
    status_code=status.HTTP_200_OK, 
    response_model=RejectedPostulationsResponse
)
async def get_rejected_postulations_count_by_id(db: DatabaseSession, opportunity_id: int):
    return opportunity_service.get_rejected_postulations_count_by_id(db, opportunity_id)


@opportunity_router.get("/opportunities/rejected-postulations-count-by-dates", response_model=list[RejectedPostulationsResponse])
async def rejected_postulations_count_by_date_range(
    db: DatabaseSession,
    from_date: Optional[datetime] = Query(None, description="Fecha de inicio"),
    to_date: Optional[datetime] = Query(None, description="Fecha de fin"),
):
    return opportunity_service.get_rejected_postulations_count_by_date_range(db, from_date, to_date)

@opportunity_router.get("opportunities/indicators-by-date-range", response_model=IndicatorsPostulationsResponse)
async def get_indicators_by_date_range(
    db: DatabaseSession,
    from_date: Optional[datetime] = Query(None, description="Fecha de inicio"),
    to_date: Optional[datetime] = Query(None, description="Fecha de fin"),
):
    return opportunity_service.get_indicators_by_date_range(db, from_date, to_date)