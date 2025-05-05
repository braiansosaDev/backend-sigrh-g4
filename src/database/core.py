from contextlib import asynccontextmanager
from typing import Annotated
from fastapi import Depends
from sqlmodel import SQLModel, Session, create_engine
from fastapi import FastAPI
from dotenv import load_dotenv
from os import getenv
import logging

logger = logging.getLogger('uvicorn.info')

load_dotenv()
use_test_database: str | None = getenv("USE_TEST_DATABASE")
if use_test_database is None:
    logger.info("USE_TEST_DATABASE not found, using postgresql database...")
    url: str = str(getenv("DATABASE_URL"))
elif use_test_database.lower() == 'true':
    logger.info('Using test database')
    url: str = str(getenv("TEST_DATABASE_URL"))
else:
    logger.info('Using PostgreSQL database')
    url = str(getenv("DATABASE_URL"))
engine = create_engine(url)


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
