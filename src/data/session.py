from contextlib import asynccontextmanager
from typing import Annotated
from fastapi import Depends
from sqlmodel import SQLModel, Session, create_engine
from fastapi import FastAPI

url = "sqlite:///src/data/hr-management.db"
engine = create_engine(url, connect_args={"check_same_thread": False})


def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


SessionDep = Annotated[Session, Depends(get_session)]
