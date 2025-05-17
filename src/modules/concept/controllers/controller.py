from typing import List
from fastapi import APIRouter, status
from src.database.core import DatabaseSession
from src.modules.concept.schemas import schemas
from src.modules.concept.services import service

concept_router = APIRouter(prefix="/concept", tags=["Concept"])


@concept_router.get(
    "/", response_model=List[schemas.ConceptResponse], status_code=status.HTTP_200_OK
)
async def read_concepts(db: DatabaseSession):
    """
    docstring
    """
    return service.get_concepts(db)


@concept_router.post(
    "/", response_model=schemas.ConceptResponse, status_code=status.HTTP_201_CREATED
)
async def create_concept(db: DatabaseSession, request: schemas.ConceptRequest):
    """
    docstring
    """
    return service.post_concept(db, request)


@concept_router.patch(
    "/{concept_id}",
    response_model=schemas.ConceptResponse,
    status_code=status.HTTP_200_OK,
)
async def update_concept(
    db: DatabaseSession, concept_id: int, request: schemas.ConceptRequest
):
    """
    docstring
    """
    return service.patch_concept(db, concept_id, request)


@concept_router.delete("/{concept_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_concept(db: DatabaseSession, concept_id: int):
    """
    docstring
    """
    return service.delete_concept(db, concept_id)
