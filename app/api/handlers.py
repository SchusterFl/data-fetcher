from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from app.models.handler import HandlerCreate, HandlerRead, HandlerUpdate
from app.services.handler import HandlerService

router = APIRouter()

@router.post("/", response_model=HandlerRead, status_code=status.HTTP_201_CREATED)
async def create_handler(
    handler: HandlerCreate,
    service: HandlerService = Depends(),
):
    """
    Erstellt einen neuen Datenhandler.
    """
    return await service.create(handler)

@router.get("/", response_model=List[HandlerRead])
async def read_handlers(
    skip: int = 0,
    limit: int = 100,
    service: HandlerService = Depends(),
):
    """
    Gibt eine Liste aller Datenhandler zurück.
    """
    return await service.get_all(skip=skip, limit=limit)

@router.get("/{handler_id}", response_model=HandlerRead)
async def read_handler(
    handler_id: int,
    service: HandlerService = Depends(),
):
    """
    Gibt einen einzelnen Datenhandler anhand seiner ID zurück.
    """
    handler = await service.get_by_id(handler_id)
    if handler is None:
        raise HTTPException(status_code=404, detail="Datenhandler nicht gefunden")
    return handler

@router.put("/{handler_id}", response_model=HandlerRead)
async def update_handler(
    handler_id: int,
    handler: HandlerUpdate,
    service: HandlerService = Depends(),
):
    """
    Aktualisiert einen vorhandenen Datenhandler.
    """
    db_handler = await service.get_by_id(handler_id)
    if db_handler is None:
        raise HTTPException(status_code=404, detail="Datenhandler nicht gefunden")
    return await service.update(handler_id, handler)

@router.delete("/{handler_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_handler(
    handler_id: int,
    service: HandlerService = Depends(),
):
    """
    Löscht einen Datenhandler.
    """
    handler = await service.get_by_id(handler_id)
    if handler is None:
        raise HTTPException(status_code=404, detail="Datenhandler nicht gefunden")
    await service.delete(handler_id)
    return None

@router.post("/{handler_id}/test", status_code=status.HTTP_200_OK)
async def test_handler(
    handler_id: int,
    test_data: dict,
    service: HandlerService = Depends(),
):
    """
    Testet einen Datenhandler mit Testdaten.
    """
    handler = await service.get_by_id(handler_id)
    if handler is None:
        raise HTTPException(status_code=404, detail="Datenhandler nicht gefunden")
    
    try:
        result = await service.test_handler(handler, test_data)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Fehler beim Testen: {str(e)}")