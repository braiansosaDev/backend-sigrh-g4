from fastapi import APIRouter, status
from typing import List
from src.database.core import DatabaseSession
from src.modules.employees.schemas.job_models import JobResponse, CreateJob, UpdateJob
from src.modules.employees.services import job_service

job_router = APIRouter(prefix="/jobs", tags=["Jobs"])

"""Enpoint para buscar un puesto o job por su ID. 
Returns:
    JobResponse: Devuelve los datos del puesto o job.
"""

@job_router.get("/", response_model=List[JobResponse], status_code=status.HTTP_200_OK)
async def get_all_jobs(db: DatabaseSession):
    return job_service.get_all_jobs(db)

@job_router.get("/{job_id}", response_model=JobResponse, status_code=status.HTTP_200_OK)
async def get_job_by_id(db: DatabaseSession, job_id: int):
    return job_service.get_job_by_id(db, job_id)

"""Enpoint para crear unun puesto o job nuevo.
Returns:
    JobResponse: Devuelve los datos de un puesto o job.
"""
@job_router.post("/create", response_model=JobResponse, status_code=status.HTTP_201_CREATED)
async def create_job(db: DatabaseSession, create_job_request: CreateJob):
    return job_service.create_job(db, create_job_request)

"""Endpoint para actualizar los datos de un puesto o job.
Returns:
    JobResponse: Devuelve los datos de un puesto o job actualizado.
"""
@job_router.patch("/{job_id}", response_model=JobResponse, status_code=status.HTTP_200_OK)
async def update_job(job_id: int, update: UpdateJob, db: DatabaseSession):
    return job_service.update_job(db,job_id, update)

"""Endpoint para eliminar un puesto o job.
Returns:
    CODE: 204
"""
@job_router.delete("/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_job(job_id: int, db: DatabaseSession):
    return job_service.delete_job(db, job_id)

