from fastapi import APIRouter
import logging

logger = logging.getLogger("uvicorn.error")
concept_router = APIRouter(prefix="/concept", tags=["Concept"])


@concept_router.get("/")
async def read_concepts():
    """
    docstring
    """
    pass


@concept_router.post("/")
async def create_concept():
    """
    docstring
    """
    pass


@concept_router.patch("/{concept_id}")
async def update_concept(concept_id: int):
    """
    docstring
    """
    pass


@concept_router.delete("/{concept_id}")
async def delete_concept(concept_id: int):
    """
    docstring
    """
    pass
