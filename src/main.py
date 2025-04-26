from fastapi import FastAPI
from .database.core import lifespan
from .employees.controllers.employee_controller import employee_router

app = FastAPI(
    prefix="/api/v1/", lifespan=lifespan, title="Talent Management API", version="0.1.0"
)
app.include_router(employee_router)
