from src.database.core import DatabaseSession
from src.modules.employees.schemas.country_models import CreateCountry, UpdateCountry
from src.modules.employees.models.country import Country
from fastapi import HTTPException, status
from sqlmodel import select

def get_all_countries(db: DatabaseSession):
    return db.exec(select(Country)).all()

def get_country_by_id(db: DatabaseSession, country_id: int) -> Country:
    return db.exec(
        select(Country)
        .where(Country.id == country_id)
    ).one_or_none()


def create_country(db: DatabaseSession,create_country_request: CreateCountry,) -> Country:
    db_country = Country(
        name=create_country_request.name,
    )
    db.add(db_country)
    db.commit()
    db.refresh(db_country)
    return db_country


def update_country(db: DatabaseSession,update_country_request: UpdateCountry, country_id: int) -> Country:
    country = db.exec(
        select(Country).where(Country.id == country_id)
    ).one_or_none()

    if country is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Country not found."
        )

    country.name = update_country_request.name
    db.add(country)
    db.commit()
    db.refresh(country)
    return country
    

def delete_country(db: DatabaseSession,country_id: int) -> None:
    country = db.exec(
        select(Country).where(Country.id == country_id)
    ).one_or_none()

    if country is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Country not found."
        )

    db.delete(country)
    db.commit()
