from fastapi import APIRouter
import logging

logger = logging.getLogger("uvicorn.error")
employee_hours_router = APIRouter(prefix="/employee_hours", tags=["Employee hours"])


@employee_hours_router.get("/")
async def read_employee_hours():
    """
    docstring
    """
    pass


@employee_hours_router.post("/")
async def create_employee_hours():
    """
    docstring
    """
    pass


@employee_hours_router.patch("/{employee_hours_id}")
async def update_employee_hours(employee_hours_id: int):
    """
    docstring
    """
    pass


@employee_hours_router.delete("/{employee_hours_id}")
async def delete_employee_hours(employee_hours_id: int):
    """
    docstring
    """
    pass
