from typing import List
from fastapi import APIRouter, status
from src.database.core import DatabaseSession
from src.modules.shift.services import services
from src.modules.shift.schemas import schemas
import logging

logger = logging.getLogger("uvicorn.error")
shift_router = APIRouter(prefix="/shift", tags=["Shift"])


@shift_router.get(
    "/", response_model=List[schemas.ShiftResponse], status_code=status.HTTP_200_OK
)
async def read_shift(db: DatabaseSession):
    """
    docstring
    """
    return services.get_shifts(db)


@shift_router.post(
    "/", response_model=schemas.ShiftResponse, status_code=status.HTTP_201_CREATED
)
async def create_shift(db: DatabaseSession, request: schemas.ShiftRequest):
    """
    docstring
    """
    return services.post_shift(db, request)


@shift_router.patch(
    "/{shift_id}", response_model=schemas.ShiftResponse, status_code=status.HTTP_200_OK
)
async def update_shift(
    db: DatabaseSession, shift_id: int, request: schemas.ShiftRequest
):
    """
    docstring
    """
    return services.patch_shift(db, shift_id, request)


@shift_router.delete("/{shift_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_shift(db: DatabaseSession, shift_id: int):
    """
    docstring
    """
    return services.delete_shift(db, shift_id)
