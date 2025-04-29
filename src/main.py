from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database.core import lifespan
from .employees.controllers.employee_controller import employee_router

app = FastAPI(
    prefix="/api/v1/", lifespan=lifespan, title="Talent Management API", version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Podés usar ["*"] para permitir todos (no recomendado en producción)
    allow_credentials=True,
    allow_methods=["*"],  # ["GET", "POST", ...] si querés limitar
    allow_headers=["*"],
)

app.include_router(employee_router)
