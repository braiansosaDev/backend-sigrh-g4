from fastapi import FastAPI
from src.database.core import lifespan
from src.employees.controllers.employee_controller import employee_router
from src.employees.controllers.documents_controller import documents_router
from src.employees.controllers.work_history_controller import work_history_router


app = FastAPI(
    root_path="/api/v1",
    lifespan=lifespan,
    title="Talent Management API",
    version="0.1.0",
)
app.include_router(employee_router)
app.include_router(work_history_router)
app.include_router(documents_router)
