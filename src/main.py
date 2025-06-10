from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.database.core import lifespan
from src.modules.employees.controllers.employee_controller import employee_router
from src.modules.employees.controllers.documents_controller import documents_router
from src.modules.employees.controllers.work_history_controller import (
    work_history_router,
)
from src.modules.opportunity.controllers.job_opportunity_controller import (
    opportunity_router,
)
from src.modules.ability.controllers.ability_controller import ability_router
from src.modules.employees.controllers.country_controller import country_router
from src.modules.employees.controllers.state_controller import state_router
from src.modules.employees.controllers.sector_controller import sector_router
from src.modules.employees.controllers.job_controller import job_router
from src.modules.postulation.controllers.postulation_controller import (
    postulation_router,
)
from src.modules.role.controllers.role_controller import role_router
from src.modules.role.controllers.permission_controller import permission_router
from src.auth.auth_controller import auth_router
from src.cv_matching.controller import matcher_router

from src.modules.face_recognition.controllers.face_recognition_controller import face_recognition_router

from src.modules.employee_hours.controllers.controller import employee_hours_router
from src.modules.clock_events.controllers.controller import clock_events_router
from src.modules.concept.controllers.controller import concept_router
from src.modules.shift.controllers.controller import shift_router
from src.modules.payroll_calculator.controller import payroll_router
from src.modules.leave.controllers.leave_controller import leave_router

from src.modules.configuration.config_controller import config_router

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
app.include_router(opportunity_router)
app.include_router(ability_router)
app.include_router(country_router)
app.include_router(state_router)
app.include_router(sector_router)
app.include_router(job_router)
app.include_router(postulation_router)
app.include_router(auth_router)
app.include_router(matcher_router)
app.include_router(role_router)
app.include_router(permission_router)
app.include_router(face_recognition_router)
app.include_router(employee_hours_router)
app.include_router(clock_events_router)
app.include_router(concept_router)
app.include_router(shift_router)
app.include_router(payroll_router)
app.include_router(leave_router)
app.include_router(config_router)
