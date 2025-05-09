from fastapi import APIRouter, status
from src.database.core import DatabaseSession
from src.cv_matching import matcher_service
from src.cv_matching import schema
from typing import List
from src.modules.opportunity.schemas.job_opportunity_schemas import (
    JobOpportunityResponse,
)


matcher_router = APIRouter(prefix="/matcher", tags=["Skills matcher"])


# @matcher_router.get(
#     "/{job_opportunity_id}",
#     status_code=status.HTTP_200_OK,
#     response_model=JobOpportunityResponse,
# )
# async def get_all_abilities(db: DatabaseSession, job_opportunity_id: int):
#     return matcher_service.get_all_abilities(db, job_opportunity_id)


# @matcher_router.get(
#     "/{job_opportunity_id}",
#     status_code=status.HTTP_200_OK,
#     response_model=List[schema.PostulationResume],
# )
# async def get_job_postulations(db: DatabaseSession, job_opportunity_id: int):
#     return matcher_service.get_all_postulations(db, job_opportunity_id)


@matcher_router.get(
    "/{job_opportunity_id}",
    status_code=status.HTTP_200_OK,
    response_model=List[schema.MatcherResponse],
)
async def evaluate_candidates(db: DatabaseSession, job_opportunity_id: int):
    return matcher_service.evaluate_candidates(db, job_opportunity_id)
