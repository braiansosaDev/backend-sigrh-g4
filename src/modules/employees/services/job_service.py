from src.database.core import DatabaseSession
from src.modules.employees.schemas.job_models import CreateJob, UpdateJob
from src.modules.employees.models.job import Job
from fastapi import HTTPException, status
from sqlmodel import select

def get_all_jobs(db: DatabaseSession):
    return db.exec(select(Job)).all()

def get_job_by_id(db: DatabaseSession, job_id: int) -> Job:
    return db.exec(
        select(Job)
        .where(Job.id == job_id)
    ).one_or_none()

def create_job(db: DatabaseSession,create_job_request: CreateJob,) -> Job:
    db_job = Job(
        name=create_job_request.name,
        sector_id=create_job_request.sector_id
    )
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job


def update_job(db: DatabaseSession,job_id: int,update_job_request: UpdateJob) -> Job:
    job = db.exec(
        select(Job).where(Job.id == job_id)
    ).one_or_none()

    if job is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Job not found."
        )

    job.name = update_job_request.name
    job.sector_id = update_job_request.sector_id
    db.add(job)
    db.commit()
    db.refresh(job)
    return job
    

def delete_job(db: DatabaseSession,job_id: int) -> None:
    job = db.exec(
        select(Job).where(Job.id == job_id)
    ).one_or_none()

    if job is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Job not found."
        )

    db.delete(job)
    db.commit()
