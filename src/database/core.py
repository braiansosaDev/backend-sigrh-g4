from contextlib import asynccontextmanager
from typing import Annotated
from fastapi import Depends
from sqlalchemy.event import listen
from sqlmodel import SQLModel, Session, create_engine
from fastapi import FastAPI
from dotenv import load_dotenv
from os import getenv
import logging

# IMPORTAR LAS TABLAS
from src.modules.ability.models.ability_models import AbilityModel
from src.modules.clock_events.models.models import ClockEvents
from src.modules.concept.models.models import Concept
from src.modules.employee_hours.models.models import EmployeeHours
from src.modules.employees.models.country import Country
from src.modules.employees.models.documents import Document
from src.modules.employees.models.employee import Employee
from src.modules.employees.models.job import Job
from src.modules.employees.models.sector import Sector
from src.modules.employees.models.state import State
from src.modules.employees.models.work_history import WorkHistory
from src.modules.postulation.models.postulation_models import Postulation
from src.modules.shift.models.models import Shift
from src.modules.configuration.config_models import Configuration
from src.modules.leave.models.leave_models import Leave
from src.modules.opportunity.models.job_opportunity_models import (
    JobOpportunityAbility,
    JobOpportunityModel,
)

logger = logging.getLogger("uvicorn.info")

load_dotenv()
use_test_database: str | None = getenv("USE_TEST_DATABASE")
if use_test_database is None:
    logger.info("USE_TEST_DATABASE not found, using postgresql database...")
    url: str = str(getenv("DATABASE_URL"))
elif use_test_database.lower() == "true":
    logger.info("Using test database")
    url: str = str(getenv("TEST_DATABASE_URL"))
else:
    logger.info("Using PostgreSQL database")
    url = str(getenv("DATABASE_URL"))
engine = create_engine(url)
logger.info(f"Engine name: {engine.name}")


def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


if engine.name == "sqlite":
    logger.info("Enabling sqlite foreign key support")
    listen(engine, "connect", set_sqlite_pragma)


def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


DatabaseSession = Annotated[Session, Depends(get_session)]
