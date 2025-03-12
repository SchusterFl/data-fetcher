from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from app.models.output import OutputCreate, OutputRead, OutputUpdate
from app.services.output import OutputService

router = APIRouter()

@router.post("/", response_model=OutputRead, status_code=status.HTTP_201_CREATED)
async def create_output(
    output: OutputCreate,
    service: OutputService = Depends(),
):
    """
    Erstellt eine neue Ausgabekonfiguration.
    """
    return await service.create(output)

@router.get("/", response_model=List[OutputRead])
async def read_outputs(
    skip: int = 0,
    limit: int = 100,
    service: OutputService = Depends(),
):
    """
    Gibt eine Liste aller Ausgabekonfigurationen zurück.
    """
    return await service.get_all(skip=skip, limit=limit)

@router.get("/{output_id}", response_model=OutputRead)
async def read_output(
    output_id: int,
    service: OutputService = Depends(),
):
    """
    Gibt eine einzelne Ausgabekonfiguration anhand ihrer ID zurück.
    """
    output = await service.get_by_id(output_id)
    if output is None:
        raise HTTPException(status_code=404, detail="Ausgabekonfiguration nicht gefunden")
    return output

@router.put("/{output_id}", response_model=OutputRead)
async def update_output(
    output_id: int,
    output: OutputUpdate,
    service: OutputService = Depends(),
):
    """
    Aktualisiert eine vorhandene Ausgabekonfiguration.
    """
    db_output = await service.get_by_id(output_id)
    if db_output is None:
        raise HTTPException(status_code=404, detail="Ausgabekonfiguration nicht gefunden")
    return await service.update(output_id, output)

@router.delete("/{output_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_output(
    output_id: int,
    service: OutputService = Depends(),
):
    """
    Löscht eine Ausgabekonfiguration.
    """
    output = await service.get_by_id(output_id)
    if output is None:
        raise HTTPException(status_code=404, detail="Ausgabekonfiguration nicht gefunden")
    await service.delete(output_id)
    return None