from src.database.core import DatabaseSession
from src.modules.opportunity.models.job_opportunity_models import (
    JobOpportunityModel,
    JobOpportunityIdModel,
    JobOpportunityAbility,
)
from sqlmodel import select
from typing import Sequence
from src.modules.opportunity.schemas.job_opportunity_schemas import (
    JobOpportunityRequest,
    JobOpportunityResponse,
)
from src.modules.ability.models.ability_models import AbilityModel
from src.modules.ability.schemas.ability_schemas import AbilityPublic
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
import logging


logger = logging.getLogger("uvicorn.error")


def get_all_opportunities_with_abilities(db: DatabaseSession) -> Sequence[JobOpportunityModel]:
    opportunities = db.exec(select(JobOpportunityModel)).all()
    result = []
    for opportunity in opportunities:
        opportunity_with_id = JobOpportunityResponse(**opportunity.dict())
        result.append(get_opportunity_with_abilities(db, opportunity_with_id.id))
    return result


def create_opportunity(
    db: DatabaseSession, request: JobOpportunityRequest
) -> JobOpportunityResponse:
    try:
        db_opportunity = JobOpportunityModel(**request.dict())
        abilities: list[AbilityPublic] = request.job_opportunity_abilities
        if len(abilities) == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="You need to provide at least one ability.",
            )
        abilities_ids = set()
        for ability in abilities:
            db_ability = db.exec(
                select(AbilityModel)
                .where(AbilityModel.id == ability.id)
                .where(AbilityModel.name == ability.name)
                .where(AbilityModel.description == ability.description)
            ).one_or_none()
            if db_ability is None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"The following ability does not exist: {ability.model_dump_json()}",
                )
            else:
                abilities_ids.add(db_ability.id)

        if len(abilities_ids) != len(abilities):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="There are duplicated abilities.")

        db.add(db_opportunity)
        db.commit()
        db.refresh(db_opportunity)
        logger.info(f"New JobOpportunity created with ID: {db_opportunity.id}")

    except IntegrityError as e:
        db.rollback()
        detail = "Bad request"
        if e.orig is not None:
            logger.info(e.orig)
            if "violates foreign key constraint " in str(e.orig):
                detail = "Some of the provided IDs do not exist."
            else:
                logger.info(e.orig)
        else:
            logger.info(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)

    try:
        opportunity = JobOpportunityIdModel(**db_opportunity.dict())
        for ability in abilities:
            logger.info(
                f"Adding JobOpportunityAbility with JobOpportunity id {db_opportunity.id}"
            )
            db.add(
                JobOpportunityAbility(
                    job_opportunity_id=opportunity.id, ability_id=ability.id
                )
            )
        db.commit()
        return get_opportunity_with_abilities(db, opportunity.id)
    except IntegrityError as e:
        db.rollback()
        logger.error("Adding JobOpportunityAbility failed, removing JobOpportunity...")
        logger.error(e)
        try:
            db.delete(db_opportunity)
            db.commit()
        except IntegrityError as e:
            logger.error(
                f"Critical error: Incompletely created JobOpportunity with id {db_opportunity.id} could not be deleted. Please fix the problem manually."
            )
            logger.error(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


def delete_opportunity(db: DatabaseSession, opportunity_id: int):
    opportunity = get_opportunity_by_id(db, opportunity_id)
    if opportunity is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The opportunity with id {opportunity_id} does not exist.",
        )

    try:
        job_opportunity_ability = db.exec(
            select(JobOpportunityAbility).where(
                JobOpportunityAbility.job_opportunity_id == opportunity.id
            )
        ).all()
        for item in job_opportunity_ability:
            db.delete(item)
        db.commit()
        db.delete(opportunity)
        db.commit()
    except IntegrityError as e:
        logger.info(e)
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Could not delete opportunity with id {opportunity.id}",
        )


def get_opportunity_with_abilities(
    db: DatabaseSession, opportunity_id: int
) -> JobOpportunityResponse:
    try:
        opportunity = get_opportunity_by_id(db, opportunity_id)
        if opportunity is None:
            raise HTTPException(
                status_code=400,
                detail=f"The opportunity with id {opportunity_id} does not exist.",
            )
        job_opportunity_abilities = db.exec(
            select(JobOpportunityAbility.ability_id)
            .where(JobOpportunityAbility.job_opportunity_id == opportunity_id)
            .join(AbilityModel)
        ).all()
        abilities = []
        for id in job_opportunity_abilities:
            db_ability = db.exec(select(AbilityModel).where(AbilityModel.id == id)).one()
            ability = AbilityPublic(**db_ability.dict())
            abilities.append(ability)
        response = JobOpportunityResponse(
            **opportunity.dict(), job_opportunity_abilities=abilities
        )
        return response
    except IntegrityError as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


def get_opportunity_by_id(
    db: DatabaseSession, opportunity_id: int
) -> JobOpportunityModel | None:
    return db.exec(
        select(JobOpportunityModel).where(JobOpportunityModel.id == opportunity_id)
    ).one_or_none()
