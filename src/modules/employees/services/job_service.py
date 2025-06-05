from src.database.core import DatabaseSession
from src.modules.employees.schemas.job_models import CreateJob, UpdateJob
from src.modules.employees.models.job import Job
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlmodel import select
from typing import cast, Any
import logging

logger = logging.getLogger("uvicorn.error")


def get_all_jobs(db: DatabaseSession):
    return db.exec(
        select(Job)
        .order_by(cast(Any, Job.id))
    ).all()


def get_job_by_id_or_none(db: DatabaseSession, job_id: int) -> Job | None:
    return db.exec(select(Job).where(Job.id == job_id)).one_or_none()


def get_job_by_id(db: DatabaseSession, job_id: int) -> Job:
    result = get_job_by_id_or_none(db, job_id)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"El Job con ID {job_id} no existe."
        )
    return result

def create_job(db: DatabaseSession, create_job_request: CreateJob) -> Job:
    db_job = Job(
        name=create_job_request.name,
        sector_id=create_job_request.sector_id
    )

    try:
        db.add(db_job)
        db.commit()
        db.refresh(db_job)
        return db_job
    except IntegrityError:
        db.rollback()
        logger.error(f"An unexpected error occurred while creating Job with data {create_job_request.model_dump_json()}")
        raise


def update_job(db: DatabaseSession, job_id: int, update_job_request: UpdateJob) -> Job:
    db_job = get_job_by_id(db, job_id)

    for attr, value in update_job_request.dict(exclude_unset=True).items():
        setattr(db_job, attr, value)

    try:
        db.add(db_job)
        db.commit()
        db.refresh(db_job)
        return db_job
    except IntegrityError:
        db.rollback()
        logger.error(f"An unexpected error occurred while updating Job with ID {job_id} and data {update_job_request.model_dump_json()}")
        raise


def delete_job(db: DatabaseSession, job_id: int) -> None:
    db_job = get_job_by_id(db, job_id)

    try:
        db.delete(db_job)
        db.commit()
    except IntegrityError:
        db.rollback()
        logger.error(f"An unexpected IntegrityError occurred while deleting Job with ID {job_id}")
        raise
