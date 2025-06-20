from datetime import date
from fastapi import APIRouter, Query, status
from src.database.core import DatabaseSession
from src.modules.postulation.schemas.postulation_schemas import (
    PostulationCreate,
    PostulationResponse,
    PostulationUpdate,
)
from src.modules.postulation.services import postulation_service


postulation_router = APIRouter(prefix="/postulations", tags=["Postulations"])


@postulation_router.get(path="/stats/", response_model=list[dict[str, int]])
async def get_suitability_count(
    session: DatabaseSession,
    from_date: date | None = Query(None),
    to_date: date | None = Query(None),
    job_opportunity_id: int | None = Query(None),
):
    return postulation_service.get_suitability_count(
        session, from_date, to_date, job_opportunity_id # type: ignore
    )


# @postulation_router.get(path="/stats")
# async def get_status_count():
#     pass


@postulation_router.get("/", response_model=list[PostulationResponse])
async def get_all_postulations(
    db: DatabaseSession, job_opportunity_id: int | None = None
):
    return postulation_service.get_all_postulations(db, job_opportunity_id)


@postulation_router.get("/can_create", response_model=bool)
async def can_create(db: DatabaseSession, job_opportunity_id: int):
    return postulation_service.can_create(db, job_opportunity_id)


@postulation_router.get("/{postulation_id}", response_model=PostulationResponse)
async def get_postulation(db: DatabaseSession, postulation_id: int):
    return postulation_service.get_postulation_by_id_or_bad_request(db, postulation_id)


@postulation_router.post(
    "/create", status_code=status.HTTP_201_CREATED, response_model=PostulationResponse
)
async def create_postulation(db: DatabaseSession, body: PostulationCreate):
    return postulation_service.create_postulation(db, body)


@postulation_router.delete("/{postulation_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_postulation(db: DatabaseSession, postulation_id: int):
    return postulation_service.delete_postulation(db, postulation_id)


@postulation_router.patch("/{postulation_id}", response_model=PostulationResponse)
async def update_postulation(
    db: DatabaseSession, postulation_id: int, body: PostulationUpdate
):
    return postulation_service.update_postulation(db, postulation_id, body)
