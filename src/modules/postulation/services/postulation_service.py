from src.database.core import DatabaseSession
from src.modules.postulation.models.postulation_models import Postulation
from src.modules.postulation.schemas.postulation_schemas import (
    PostulationCreate,
    PostulationUpdate,
)
from src.modules.opportunity.models.job_opportunity_models import JobOpportunityModel
from src.modules.opportunity.services import opportunity_service
from sqlmodel import select, col
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from typing import Sequence, cast, Any
import logging

logger = logging.getLogger("uvicorn.error")

MAX_POSTULATIONS_PER_OPPORTUNITY = 1000


def get_postulation_count(db: DatabaseSession, job_opportunity_id: int) -> int:
    opportunity: JobOpportunityModel | None = opportunity_service.get_opportunity_by_id(
        db, job_opportunity_id
    )
    if opportunity is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The job opportunity with ID {job_opportunity_id} does not exist.",
        )

    return db.exec(
        select(func.count(col(Postulation.id))).where(
            Postulation.job_opportunity_id == job_opportunity_id
        )
    ).one()


def can_create(db: DatabaseSession, job_opportunity_id: int) -> bool:
    count = get_postulation_count(db, job_opportunity_id)
    return count < MAX_POSTULATIONS_PER_OPPORTUNITY


def get_all_postulations(
    db: DatabaseSession, job_opportunity_id: int | None = None
) -> Sequence[Postulation]:
    query = select(Postulation)
    if job_opportunity_id is not None:
        query = query.where(Postulation.job_opportunity_id == job_opportunity_id)
    return db.exec(
        query.order_by(cast(Any, Postulation.id))
    ).all()


def get_postulation_by_id(
    db: DatabaseSession, postulation_id: int
) -> Postulation | None:
    return db.exec(
        select(Postulation).where(Postulation.id == postulation_id)
    ).one_or_none()


def get_postulation_by_id_or_bad_request(db: DatabaseSession, postulation_id: int):
    postulation = get_postulation_by_id(db, postulation_id)

    if postulation is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"The postulation with ID {postulation_id} does not exist.",
        )

    return postulation


def create_postulation(db: DatabaseSession, request: PostulationCreate) -> Postulation:
    try:
        if not can_create(db, request.job_opportunity_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Se alcanzó el límite de postulaciones ({MAX_POSTULATIONS_PER_OPPORTUNITY}) para esta convocatoria",
            )

        postulation = Postulation(**request.model_dump())

        db.add(postulation)
        db.commit()
        db.refresh(postulation)
        return postulation
    except IntegrityError as e:
        db.rollback()

        if "foreign key constraint" in str(e.orig).lower():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Some of the provided IDs do not exist.",
            )
        else:
            logger.error(
                f"Unexpected error occurred while creating postulation with data {request.model_dump()}"
            )
            raise


def delete_postulation(db: DatabaseSession, postulation_id: int) -> None:
    try:
        postulation = get_postulation_by_id_or_bad_request(db, postulation_id)
        db.delete(postulation)
        db.commit()
    except IntegrityError as e:
        logger.error(
            f"Unexpected IntegrityError while trying to delete postulation with ID {postulation_id}"
        )
        logger.error(e)
        raise


def update_postulation(
    db: DatabaseSession, postulation_id: int, body: PostulationUpdate
) -> Postulation:
    postulation = get_postulation_by_id_or_bad_request(db, postulation_id)

    body_dict = body.model_dump(exclude_unset=True)

    if "job_opportunity_id" in body_dict:
        if not can_create(db, body_dict["job_opportunity_id"]):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Se alcanzó el límite de postulaciones ({MAX_POSTULATIONS_PER_OPPORTUNITY}) para esta convocatoria",
            )

    for attr, value in body_dict.items():
        if hasattr(postulation, attr):
            setattr(postulation, attr, value)

    try:
        db.add(postulation)
        db.commit()
        db.refresh(postulation)
        return postulation
    except IntegrityError as e:
        db.rollback()
        logger.error(
            f"Unexpected IntegrityError while updating postulation with ID {postulation_id}"
        )
        logger.error(e)
        raise
