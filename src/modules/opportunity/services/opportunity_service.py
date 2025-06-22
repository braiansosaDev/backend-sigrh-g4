from datetime import date, datetime
import copy
from time import time
from src.database.core import DatabaseSession
from src.modules.auth.token import TokenDependency
from src.modules.logs import log_schemas, log_service
from src.modules.logs.log_model import EntityType
from src.modules.opportunity.models.job_opportunity_models import (
    JobOpportunityModel,
    JobOpportunityIdModel,
    JobOpportunityAbility,
)
from sqlmodel import func, select
from typing import Optional, Sequence
from src.modules.opportunity.models.job_opportunity_models import JobOpportunityModel
from src.modules.opportunity.schemas.job_opportunity_schemas import (
    JobOpportunityActiveCountRequest,
    JobOpportunityActiveCountResponse,
    JobOpportunityAndPostulationsResponse,
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

from src.modules.postulation.models.postulation_models import Postulation
from src.modules.postulation.schemas.postulation_schemas import IndicatorsPostulationsResponse, PostulationStatus, RejectedOptions, RejectedPostulationsResponse
from src.modules.postulation.services.postulation_service import get_all_postulations


logger = logging.getLogger("uvicorn.error")


def count_active_opportunities(db: DatabaseSession) -> int:
    result = db.exec(
        select(func.count())
        .select_from(JobOpportunityModel)
        .where(JobOpportunityModel.status == JobOpportunityStatus.ACTIVO)
    )
    return result.one()

def get_active_inactive_opportunity_count_by_date(db: DatabaseSession, request: JobOpportunityActiveCountRequest) -> JobOpportunityActiveCountResponse:
    to_date = request.to_date.replace(hour=23, minute=59, second=59)
    active_count = db.exec(
        select(func.count())
        .select_from(JobOpportunityModel)
        .where(JobOpportunityModel.status == JobOpportunityStatus.ACTIVO)
        .where(JobOpportunityModel.created_at >= request.from_date)
        .where(JobOpportunityModel.created_at <= to_date)
    ).one()

    inactive_count = db.exec(
        select(func.count())
        .select_from(JobOpportunityModel)
        .where(JobOpportunityModel.status == JobOpportunityStatus.NO_ACTIVO)
        .where(JobOpportunityModel.created_at >= request.from_date)
        .where(JobOpportunityModel.created_at <= to_date)
    ).one()

    return JobOpportunityActiveCountResponse(
        active_count=active_count, inactive_count=inactive_count
    )


def get_all_opportunities_with_abilities(
    db: DatabaseSession,
    status: Optional[JobOpportunityStatus] = None,
    from_date: Optional[datetime] = None,
    to_date: Optional[datetime] = None,
) -> Sequence[JobOpportunityModel]:

    query = select(JobOpportunityModel)

    if status:
        query = query.where(JobOpportunityModel.status == status)
    
    if from_date:
        query = query.where(JobOpportunityModel.created_at >= from_date)

    if to_date:
        to_date = to_date.replace(hour=23, minute=59, second=59)
        query = query.where(JobOpportunityModel.created_at <= to_date)

    opportunities = db.exec(query).all()

    result = []
    for opportunity in opportunities:
        opportunity_with_id = JobOpportunityIdModel(**opportunity.dict())
        result.append(get_opportunity_with_abilities(db, opportunity_with_id.id))
    return result

def get_all_opportunities_with_postulations(
    db: DatabaseSession,
    from_date: Optional[datetime] = None,
    to_date: Optional[datetime] = None,
) -> Sequence[JobOpportunityAndPostulationsResponse]:
    query = select(JobOpportunityModel)

    if from_date:
        query = query.where(JobOpportunityModel.created_at >= from_date)

    if to_date:
        to_date = to_date.replace(hour=23, minute=59, second=59)
        query = query.where(JobOpportunityModel.created_at <= to_date)

    opportunities = db.exec(query).all()

    result = []
    for opportunity in opportunities:
        opportunity_with_id = JobOpportunityIdModel(**opportunity.dict())
        base_response = get_opportunity_with_abilities(db, opportunity_with_id.id)
        postulations = get_all_postulations(db, opportunity_with_id.id)

        response = JobOpportunityAndPostulationsResponse(
            **base_response.dict(),
            postulations=postulations
        )
        result.append(response)
    return result

def get_rejected_postulations_count_by_id(
    db: DatabaseSession, opportunity_id: int
) -> RejectedPostulationsResponse:
    
    # Validar que exista la oportunidad
    opportunity = get_opportunity_by_id(db, opportunity_id)
    if opportunity is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"La oportunidad con ID {opportunity_id} no existe."
        )
    
    # Traer todas las postulaciones NO ACEPTADAS de esa oportunidad
    rejected_postulations = db.exec(
        select(Postulation)
        .where(Postulation.job_opportunity_id == opportunity_id)
        .where(Postulation.status == PostulationStatus.NO_ACEPTADA)
    ).all()

    # Inicializar todos los motivos con 0
    conteo_motivos = {motivo.value: 0 for motivo in RejectedOptions}

    # Contar los motivos reales encontrados
    for postulation in rejected_postulations:
        motivo = postulation.motive
        if motivo in conteo_motivos:
            conteo_motivos[motivo] += 1

    # Devolver el schema
    return RejectedPostulationsResponse(opportunity_id=opportunity_id, motivos=conteo_motivos)

def get_rejected_postulations_count_by_date_range(
    db: DatabaseSession, from_date: Optional[datetime] = None,
        to_date: Optional[datetime] = None
) -> list[RejectedPostulationsResponse]:

    # 1. Obtener todas las convocatorias dentro del rango de fechas
    query = select(JobOpportunityModel)

    if from_date:
        query = query.where(JobOpportunityModel.created_at >= from_date)

    if to_date:
        to_date = to_date.replace(hour=23, minute=59, second=59)
        query = query.where(JobOpportunityModel.created_at <= to_date)

    opportunities = db.exec(query).all()

    responses = []

    for opportunity in opportunities:
        # 2. Obtener las postulaciones rechazadas de esa convocatoria
        rejected_postulations = db.exec(
            select(Postulation)
            .where(Postulation.job_opportunity_id == opportunity.id)
            .where(Postulation.status == PostulationStatus.NO_ACEPTADA)
        ).all()

        # 3. Inicializar todos los motivos con 0
        conteo_motivos = {motivo.value: 0 for motivo in RejectedOptions}

        # 4. Contar motivos existentes
        for postulation in rejected_postulations:
            motivo = postulation.motive
            if motivo in conteo_motivos:
                conteo_motivos[motivo] += 1

        # 5. Agregar respuesta
        responses.append(RejectedPostulationsResponse(
            opportunity_id=opportunity.id,
            motivos=conteo_motivos
        ))

    return responses

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
    db: DatabaseSession,
    token: TokenDependency,
    opportunity_id: int,
    request: JobOpportunityUpdate,
):
    # 1. Obtener oportunidad y permisos
    opportunity = get_opportunity_by_id(db, opportunity_id)
    if opportunity is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail=f"La oportunidad con id {opportunity_id} no existe.",
        )

    # (Opcional) podés validar aquí token/permiso, como hacés en Leave

    changes: list[str] = []  # <-- donde guardamos los cambios

    # 2. Actualizar atributos simples
    data = request.model_dump(
        exclude_unset=True, exclude={"required_abilities", "desirable_abilities"}
    )
    for field, new_val in data.items():
        if hasattr(opportunity, field):
            old_val = getattr(opportunity, field)
            if old_val != new_val:
                changes.append(f"{field}: '{old_val}' -> '{new_val}'")
                setattr(opportunity, field, new_val)

    if "required_abilities" in request.model_dump(exclude_unset=True):
        process_abilities(
            db,
            JobOpportunityAbilityImportance.REQUERIDA,
            request.required_abilities,
            opportunity_id,
            changes,
        )

    if "desirable_abilities" in request.model_dump(exclude_unset=True):
        process_abilities(
            db,
            JobOpportunityAbilityImportance.DESEADA,
            request.desirable_abilities,
            opportunity_id,
            changes,
        )

    # 4. Commit y refrescar
    db.add(opportunity)
    db.commit()
    db.refresh(opportunity)

    # 5. Crear el log en tu tabla de auditoría
    if changes:
        description = "; ".join(changes)
        log = log_service.create_log(
            db,
            log_schemas.LogCreateRequest(
                description=description,
                entity=EntityType.CONVOCATORIA,
                entity_id=opportunity_id,
                user_id=token.get("employee_id"),  # o el que corresponda
            ),
        )
        db.add(log)
        db.commit()

    # 6. Retornar la oportunidad con las habilidades cargadas
    return get_opportunity_with_abilities(db, opportunity_id)


def process_abilities(
    db: DatabaseSession,
    ability_type: JobOpportunityAbilityImportance,
    new_list: list[AbilityPublic],
    opportunity_id: int,
    changes: list[str],
):
    """Elimina viejas, añade nuevas y registra cambio si difieren."""
    prev_objs = db.exec(
        select(JobOpportunityAbility)
        .where(JobOpportunityAbility.job_opportunity_id == opportunity_id)
        .where(JobOpportunityAbility.ability_type == ability_type)
    ).all()
    prev_ids = [a.ability_id for a in prev_objs]
    new_ids = [a.id for a in new_list]

    if set(prev_ids) != set(new_ids):
        changes.append(
            f"{ability_type.name.lower()}_abilities: {prev_ids} -> {new_ids}"
        )

    # borrar antiguas y agregar nuevas
    for obj in prev_objs:
        db.delete(obj)
    for aid in new_ids:
        db.add(
            JobOpportunityAbility(
                job_opportunity_id=opportunity_id,
                ability_id=aid,
                ability_type=ability_type,
            )
        )


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


def get_indicators_by_date_range(
        db: DatabaseSession,
        from_date: Optional[datetime] = None,
        to_date: Optional[datetime] = None
) -> IndicatorsPostulationsResponse:
    """
    Obtiene indicadores de postulaciones por rango de fechas.
    """
    suitable_average: float = 0.0
    not_suitable_average: float = 0.0
    accepted_postulation_average: float = 0.0
    rejected_postulation_average: float = 0.0
    hired_postulation_average: float = 0.0
    pending_postulation_average: float = 0.0
    count_opportunities: int = 0
    count_postulations: int = 0

    query = select(JobOpportunityModel)

    if from_date:
        query = query.where(JobOpportunityModel.created_at >= from_date)

    if to_date:
        to_date = to_date.replace(hour=23, minute=59, second=59)
        query = query.where(JobOpportunityModel.created_at <= to_date)

    opportunities = db.exec(query).all()

    count_opportunities = len(opportunities)

    if count_opportunities == 0:
        return IndicatorsPostulationsResponse(
            suitable_average=suitable_average,
            not_suitable_average=not_suitable_average,
            accepted_postulation_average=accepted_postulation_average,
            rejected_postulation_average=rejected_postulation_average,
            hired_postulation_average=hired_postulation_average,
            pending_postulation_average=pending_postulation_average,
            count_opportunities=count_opportunities,
            count_postulations=count_postulations
        )
    
    # Iteramos sobre las oportunidades
    for opportunity in opportunities:
        # Contamos las postulaciones de la oportunidad
        count_postulations += db.exec(
            select(func.count())
            .select_from(Postulation)
            .where(Postulation.job_opportunity_id == opportunity.id)
        ).one()
        if count_postulations == 0:
            continue
        
        # Contamos Aptos
        suitable_average += db.exec(
            select(func.count())
            .select_from(Postulation)
            .where(Postulation.job_opportunity_id == opportunity.id)
            .where(Postulation.suitable == True)
        ).one()

        # Contamos No aptos
        not_suitable_average += db.exec(
            select(func.count())
            .select_from(Postulation)
            .where(Postulation.job_opportunity_id == opportunity.id)
            .where(Postulation.suitable == False)
        ).one()

        # Contamos Postulaciones aceptadas
        accepted_postulation_average += db.exec(
            select(func.count())
            .select_from(Postulation)
            .where(Postulation.job_opportunity_id == opportunity.id)
            .where(Postulation.status == PostulationStatus.ACEPTADA)
        ).one()

        # Contamos Postulaciones rechazadas
        rejected_postulation_average += db.exec(
            select(func.count())
            .select_from(Postulation)
            .where(Postulation.job_opportunity_id == opportunity.id)
            .where(Postulation.status == PostulationStatus.NO_ACEPTADA)
        ).one()

        # Contamos Postulaciones contratadas
        hired_postulation_average += db.exec(
            select(func.count())
            .select_from(Postulation)
            .where(Postulation.job_opportunity_id == opportunity.id)
            .where(Postulation.status == PostulationStatus.CONTRATADO)
        ).one()

        # Contamos Postulaciones pendientes
        pending_postulation_average += db.exec(
            select(func.count())
            .select_from(Postulation)
            .where(Postulation.job_opportunity_id == opportunity.id)
            .where(Postulation.status == PostulationStatus.PENDIENTE)
        ).one()

    # Calculamos los promedios
    if count_postulations > 0:
        suitable_average = round(suitable_average / count_opportunities, 2)
        not_suitable_average = round(not_suitable_average / count_opportunities, 2)
        accepted_postulation_average = round(accepted_postulation_average / count_opportunities, 2)
        rejected_postulation_average = round(rejected_postulation_average / count_opportunities, 2)
        hired_postulation_average = round(hired_postulation_average / count_opportunities, 2)
        pending_postulation_average = round(pending_postulation_average / count_opportunities, 2)
 
    return IndicatorsPostulationsResponse(
        suitable_average=suitable_average,
            not_suitable_average=not_suitable_average,
            accepted_postulation_average=accepted_postulation_average,
            rejected_postulation_average=rejected_postulation_average,
            hired_postulation_average=hired_postulation_average,
            pending_postulation_average=pending_postulation_average,
            count_opportunities=count_opportunities,
            count_postulations=count_postulations
    )