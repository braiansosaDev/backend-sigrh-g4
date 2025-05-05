from src.database.core import DatabaseSession
from src.modules.employees.schemas.sector_models import CreateSector, UpdateSector
from src.modules.employees.models.sector import Sector
from fastapi import HTTPException, status
from sqlmodel import select

def get_all_countries(db: DatabaseSession):
    return db.exec(select(Sector)).all()

def get_sector_by_id(db: DatabaseSession, sector_id: int) -> Sector:
    return db.exec(
        select(Sector)
        .where(Sector.id == sector_id)
    ).one_or_none()


def create_sector(db: DatabaseSession,create_sector_request: CreateSector,) -> Sector:
    db_sector = Sector(
        name=create_sector_request.name,
    )
    db.add(db_sector)
    db.commit()
    db.refresh(db_sector)
    return db_sector


def update_sector(db: DatabaseSession,update_sector_request: UpdateSector, sector_id: int) -> Sector:
    sector = db.exec(
        select(Sector).where(Sector.id == sector_id)
    ).one_or_none()

    if sector is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Sector not found."
        )

    sector.name = update_sector_request.name
    db.add(sector)
    db.commit()
    db.refresh(sector)
    return sector
    

def delete_sector(db: DatabaseSession,sector_id: int) -> None:
    sector = db.exec(
        select(Sector).where(Sector.id == sector_id)
    ).one_or_none()

    if sector is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Sector not found."
        )

    db.delete(sector)
    db.commit()
