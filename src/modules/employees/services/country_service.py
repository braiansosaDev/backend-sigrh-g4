from src.database.core import DatabaseSession
from src.modules.employees.schemas.country_models import CreateCountry, UpdateCountry
from src.modules.employees.models.country import Country
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlmodel import select
from typing import cast, Any
import logging

logger = logging.getLogger("uvicorn.error")

def get_all_countries(db: DatabaseSession):
    return db.exec(
        select(Country)
        .order_by(cast(Any, Country.id))
    ).all()

def get_country_by_id_or_none(db: DatabaseSession, country_id: int) -> Country | None:
    return db.exec(select(Country).where(Country.id == country_id)).one_or_none()

def get_country_by_id(db: DatabaseSession, country_id: int) -> Country:
    result = get_country_by_id_or_none(db, country_id)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Country with ID {country_id} not found."
        )
    return result


def create_country(db: DatabaseSession,create_country_request: CreateCountry,) -> Country:
    db_country = Country(
        name=create_country_request.name,
    )
    db.add(db_country)
    db.commit()
    db.refresh(db_country)
    return db_country


def update_country(db: DatabaseSession, country_id: int, update_country_request: UpdateCountry) -> Country:
    country = get_country_by_id(db, country_id)

    for attr, value in update_country_request.dict(exclude_unset=True).items():
        setattr(country, attr, value)

    try:
        db.add(country)
        db.commit()
        db.refresh(country)
        return country
    except IntegrityError:
        db.rollback()
        logger.error(f"An unexpected error occurred while updating Country with ID {country_id} and data {update_country_request.model_dump_json()}")
        raise


def delete_country(db: DatabaseSession, country_id: int) -> None:
    db_country = get_country_by_id(db, country_id)

    try:
        db.delete(db_country)
        db.commit()
    except IntegrityError:
        db.rollback()
        logger.error(f"An unexpected IntegrityError occurred while deleting Country with ID {country_id}")
        raise
