from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.database.core import lifespan
from src.modules.employees.controllers.employee_controller import employee_router
from src.modules.employees.controllers.documents_controller import documents_router
from src.modules.employees.controllers.work_history_controller import work_history_router

app = FastAPI(
    root_path="/api/v1",
    lifespan=lifespan,
    title="Talent Management API",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(employee_router)
app.include_router(work_history_router)
app.include_router(documents_router)
