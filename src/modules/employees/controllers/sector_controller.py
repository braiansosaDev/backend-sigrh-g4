from fastapi import APIRouter, status
from typing import List
from src.database.core import DatabaseSession
from src.modules.employees.schemas.sector_models import SectorResponse, CreateSector, UpdateSector
from src.modules.employees.services import sector_service

sector_router = APIRouter(prefix="/sectors", tags=["Sectors"])

"""Enpoint para buscar a un sector por su ID. 
Returns:
    SectorResponse: Devuelve los datos del sector.
"""

@sector_router.get("/", response_model=List[SectorResponse], status_code=status.HTTP_200_OK)
async def get_all_sectors(db: DatabaseSession):
    return sector_service.get_all_sectors(db)

@sector_router.get("/{sector_id}", response_model=SectorResponse, status_code=status.HTTP_200_OK)
async def get_sector_by_id(db: DatabaseSession, sector_id: int):
    return sector_service.get_sector_by_id(db, sector_id)

"""Enpoint para crear un nuevo sector.
Returns:
    SectorResponse: Devuelve los datos del sector creado.
"""
@sector_router.post("/create", response_model=SectorResponse, status_code=status.HTTP_201_CREATED)
async def create_sector(db: DatabaseSession, create_sector_request: CreateSector):
    return sector_service.create_sector(db, create_sector_request)

"""Endpoint para actualizar los datos de un sector.
Returns:
    SectorResponse: Devuelve los datos del sector actualizado.
"""
@sector_router.patch("/{sector_id}", response_model=SectorResponse, status_code=status.HTTP_200_OK)
async def update_sector(sector_id: int, update: UpdateSector, db: DatabaseSession):
    return sector_service.update_sector(db, sector_id, update)

"""Endpoint para eliminar un sector.
Returns:
    CODE: 204
"""
@sector_router.delete("/{sector_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_sector(sector_id: int, db: DatabaseSession):
    return sector_service.delete_sector(db, sector_id)

