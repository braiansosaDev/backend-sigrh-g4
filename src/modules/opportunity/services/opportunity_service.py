from src.database.core import DatabaseSession
from src.modules.opportunity.models.job_opportunity_models import (
    JobOpportunityModel,
    JobOpportunityIdModel,
    JobOpportunityAbility,
)
from sqlmodel import func, select
from typing import Sequence
from src.modules.opportunity.schemas.job_opportunity_schemas import (
    JobOpportunityRequest,
    JobOpportunityResponse,
    JobOpportunityStatus,
    JobOpportunityUpdate,
    JobOpportunityAbilityImportance,
)
from src.modules.ability.models.ability_models import AbilityModel
from src.modules.ability.schemas.ability_schemas import AbilityPublic
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
import logging


logger = logging.getLogger("uvicorn.error")


def count_active_opportunities(db: DatabaseSession) -> int:
    result = db.exec(
        select(func.count())
        .select_from(JobOpportunityModel)
        .where(JobOpportunityModel.status == JobOpportunityStatus.ACTIVO)
    )
    return result.one()


def get_all_opportunities_with_abilities(
    db: DatabaseSession,
) -> Sequence[JobOpportunityModel]:
    opportunities = db.exec(select(JobOpportunityModel)).all()
    result = []
    for opportunity in opportunities:
        opportunity_with_id = JobOpportunityIdModel(**opportunity.dict())
        result.append(get_opportunity_with_abilities(db, opportunity_with_id.id))
    return result


def validate_job_opportunity_abilities(
    db: DatabaseSession, job_opportunity_abilities: list[AbilityPublic]
) -> set[int]:
    if len(job_opportunity_abilities) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="You need to provide at least one ability.",
        )
    abilities_ids = set()
    for ability in job_opportunity_abilities:
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

    if len(abilities_ids) != len(job_opportunity_abilities):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="There are duplicated abilities.",
        )

    return abilities_ids


def create_opportunity(
    db: DatabaseSession, request: JobOpportunityRequest
) -> JobOpportunityResponse:
    try:
        db_opportunity = JobOpportunityModel(**request.model_dump())
        required_abilities: list[AbilityPublic] = request.required_abilities
        desirable_abilities: list[AbilityPublic] = request.desirable_abilities

        all_abilities_ids: set[int] = set()
        all_abilities_ids = all_abilities_ids.union(
            validate_job_opportunity_abilities(db, required_abilities)
        )
        all_abilities_ids = all_abilities_ids.union(
            validate_job_opportunity_abilities(db, desirable_abilities)
        )
        if len(all_abilities_ids) != len(required_abilities) + len(desirable_abilities):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="There are duplicated abilities",
            )

        db.add(db_opportunity)
        db.commit()
        db.refresh(db_opportunity)
        logger.info(f"New JobOpportunity created with ID: {db_opportunity.id}")

    except IntegrityError as e:
        db.rollback()
        detail = "Bad request"
        if e.orig is not None:
            logger.info(e.orig)
            if "foreign key constraint " in str(e.orig).lower():
                detail = "Some of the provided IDs do not exist."
            else:
                logger.info(e.orig)
        else:
            logger.info(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)

    try:
        opportunity = JobOpportunityIdModel(**db_opportunity.model_dump())
        for ability in required_abilities:
            logger.info(
                f"Adding required JobOpportunityAbility with JobOpportunity id {db_opportunity.id}"
            )
            db.add(
                JobOpportunityAbility(
                    job_opportunity_id=opportunity.id,
                    ability_id=ability.id,
                    ability_type=JobOpportunityAbilityImportance.REQUERIDA,
                )
            )
        for ability in desirable_abilities:
            logger.info(
                f"Adding desirable JobOpportunityAbility with JobOpportunity id {db_opportunity.id}"
            )
            db.add(
                JobOpportunityAbility(
                    job_opportunity_id=opportunity.id,
                    ability_id=ability.id,
                    ability_type=JobOpportunityAbilityImportance.DESEADA,
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


def update_opportunity(
    db: DatabaseSession, opportunity_id: int, request: JobOpportunityUpdate
):
    opportunity = get_opportunity_by_id(db, opportunity_id)

    if opportunity is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail=f"The opportunity with id {opportunity_id} does not exist.",
        )

    try:
        required_abilities_attr = "required_abilities"
        desirable_abilities_attr = "desirable_abilities"
        for attr, value in request.model_dump(
            exclude_unset=True,
            exclude=set([required_abilities_attr, desirable_abilities_attr]),
        ).items():
            if hasattr(opportunity, attr):
                setattr(opportunity, attr, value)

        all_abilities_ids: set[int] = set()
        has_required_abilities: bool = False
        has_desirable_abilities: bool = False
        if required_abilities_attr in request.model_dump(exclude_unset=True):
            has_required_abilities = True
            all_abilities_ids = all_abilities_ids.union(
                validate_job_opportunity_abilities(db, request.required_abilities)
            )

        if desirable_abilities_attr in request.model_dump(exclude_unset=True):
            has_desirable_abilities = True
            all_abilities_ids = all_abilities_ids.union(
                validate_job_opportunity_abilities(db, request.desirable_abilities)
            )

        received_abilities_count = 0
        if has_required_abilities:
            received_abilities_count += len(request.required_abilities)
        if has_desirable_abilities:
            received_abilities_count += len(request.desirable_abilities)

        if len(all_abilities_ids) != received_abilities_count:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="There are duplicated abilities",
            )

        if has_required_abilities:
            previous_abilities = db.exec(
                select(JobOpportunityAbility)
                .where(JobOpportunityAbility.job_opportunity_id == opportunity_id)
                .where(
                    JobOpportunityAbility.ability_type
                    == JobOpportunityAbilityImportance.REQUERIDA
                )
            ).all()

            for previous_ability in previous_abilities:
                db.delete(previous_ability)

            for ability in request.required_abilities:
                db.add(
                    JobOpportunityAbility(
                        job_opportunity_id=opportunity_id,
                        ability_id=ability.id,
                        ability_type=JobOpportunityAbilityImportance.REQUERIDA,
                    )
                )

        if has_desirable_abilities:
            previous_abilities = db.exec(
                select(JobOpportunityAbility)
                .where(JobOpportunityAbility.job_opportunity_id == opportunity_id)
                .where(
                    JobOpportunityAbility.ability_type
                    == JobOpportunityAbilityImportance.DESEADA
                )
            ).all()

            for previous_ability in previous_abilities:
                db.delete(previous_ability)

            for ability in request.desirable_abilities:
                db.add(
                    JobOpportunityAbility(
                        job_opportunity_id=opportunity_id,
                        ability_id=ability.id,
                        ability_type=JobOpportunityAbilityImportance.DESEADA,
                    )
                )

        db.add(opportunity)
        db.commit()
        db.refresh(opportunity)

        return get_opportunity_with_abilities(db, opportunity.id)

    except IntegrityError:
        db.rollback()
        logger.error(
            f"Unexpected error while updating opportunity with id {opportunity_id}"
        )
        raise


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
        required_job_opportunity_abilities = db.exec(
            select(JobOpportunityAbility.ability_id)
            .where(JobOpportunityAbility.job_opportunity_id == opportunity_id)
            .where(
                JobOpportunityAbility.ability_type
                == JobOpportunityAbilityImportance.REQUERIDA
            )
            .join(AbilityModel)
        ).all()
        required_abilities = []
        for id in required_job_opportunity_abilities:
            db_ability = db.exec(
                select(AbilityModel).where(AbilityModel.id == id)
            ).one()
            ability = AbilityPublic(**db_ability.dict())
            required_abilities.append(ability)

        desirable_job_opportunity_abilities = db.exec(
            select(JobOpportunityAbility.ability_id)
            .where(JobOpportunityAbility.job_opportunity_id == opportunity_id)
            .where(
                JobOpportunityAbility.ability_type
                == JobOpportunityAbilityImportance.DESEADA
            )
        )
        desirable_abilities = []
        for id in desirable_job_opportunity_abilities:
            db_ability = db.exec(
                select(AbilityModel).where(AbilityModel.id == id)
            ).one()
            ability = AbilityPublic(**db_ability.dict())
            desirable_abilities.append(ability)

        response = JobOpportunityResponse(
            **opportunity.dict(),
            required_abilities=required_abilities,
            desirable_abilities=desirable_abilities,
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
