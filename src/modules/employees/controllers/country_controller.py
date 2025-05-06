from fastapi import APIRouter, status
from typing import List
from src.database.core import DatabaseSession
from src.modules.employees.schemas.country_models import CountryResponse, CreateCountry, UpdateCountry
from src.modules.employees.services import country_service

country_router = APIRouter(prefix="/countries", tags=["Countries"])

"""Enpoint para buscar a un pais por su ID. 
Returns:
    CountryResponse: Devuelve los datos del pais.
"""

@country_router.get("/", response_model=List[CountryResponse], status_code=status.HTTP_200_OK)
async def get_all_countries(db: DatabaseSession):
    return country_service.get_all_countries(db)

@country_router.get("/{country_id}", response_model=CountryResponse, status_code=status.HTTP_200_OK)
async def get_country_by_id(db: DatabaseSession,country_id: int):
    return country_service.get_country_by_id(db, country_id)

"""Enpoint para crear un nuevo pais.
Returns:
    CountryResponse: Devuelve los datos del pais creado.
"""
@country_router.post("/create", response_model=CountryResponse, status_code=status.HTTP_201_CREATED)
async def create_country(db: DatabaseSession, create_country_request: CreateCountry):
    return country_service.create_country(db, create_country_request)

"""Endpoint para actualizar los datos de un pais.
Returns:
    CountryResponse: Devuelve los datos del pais actualizado.
"""
@country_router.patch("/{country_id}", response_model=CountryResponse, status_code=status.HTTP_200_OK)
async def update_country(country_id: int, update: UpdateCountry, db: DatabaseSession):
    return country_service.update_country(db, country_id, update)

"""Endpoint para eliminar un pais.
Returns:
    CODE: 204
"""
@country_router.delete("/{country_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_country(country_id: int, db: DatabaseSession):
    return country_service.delete_country(db, country_id)

