from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from app.models.datasource import DataSourceCreate, DataSourceRead, DataSourceUpdate
from app.services.datasource import DataSourceService

router = APIRouter()

@router.post("/", response_model=DataSourceRead, status_code=status.HTTP_201_CREATED)
async def create_datasource(
    datasource: DataSourceCreate,
    service: DataSourceService = Depends(),
):
    """
    Erstellt eine neue Datenquelle.
    """
    return await service.create(datasource)

@router.get("/", response_model=List[DataSourceRead])
async def read_datasources(
    skip: int = 0,
    limit: int = 100,
    service: DataSourceService = Depends(),
):
    """
    Gibt eine Liste aller Datenquellen zurück.
    """
    return await service.get_all(skip=skip, limit=limit)

@router.get("/{datasource_id}", response_model=DataSourceRead)
async def read_datasource(
    datasource_id: int,
    service: DataSourceService = Depends(),
):
    """
    Gibt eine einzelne Datenquelle anhand ihrer ID zurück.
    """
    datasource = await service.get_by_id(datasource_id)
    if datasource is None:
        raise HTTPException(status_code=404, detail="Datenquelle nicht gefunden")
    return datasource

@router.put("/{datasource_id}", response_model=DataSourceRead)
async def update_datasource(
    datasource_id: int,
    datasource: DataSourceUpdate,
    service: DataSourceService = Depends(),
):
    """
    Aktualisiert eine vorhandene Datenquelle.
    """
    db_datasource = await service.get_by_id(datasource_id)
    if db_datasource is None:
        raise HTTPException(status_code=404, detail="Datenquelle nicht gefunden")
    return await service.update(datasource_id, datasource)

@router.delete("/{datasource_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_datasource(
    datasource_id: int,
    service: DataSourceService = Depends(),
):
    """
    Löscht eine Datenquelle.
    """
    datasource = await service.get_by_id(datasource_id)
    if datasource is None:
        raise HTTPException(status_code=404, detail="Datenquelle nicht gefunden")
    await service.delete(datasource_id)
    return None