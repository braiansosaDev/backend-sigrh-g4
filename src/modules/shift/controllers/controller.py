from fastapi import APIRouter
import logging

logger = logging.getLogger("uvicorn.error")
shift_router = APIRouter(prefix="/shift", tags=["Shift"])


@shift_router.get("/")
async def read_shift():
    """
    docstring
    """
    pass


@shift_router.post("/")
async def create_shift():
    """
    docstring
    """
    pass


@shift_router.patch("/{shift_id}")
async def update_shift(shift_id: int):
    """
    docstring
    """
    pass


@shift_router.delete("/{shift_id}")
async def delete_shift(shift_id: int):
    """
    docstring
    """
    pass
