from fastapi import APIRouter

from app.api import datasources, handlers, outputs

router = APIRouter()

# Einbinden der Modul-Router
router.include_router(datasources.router, prefix="/datasources", tags=["Datenquellen"])
router.include_router(handlers.router, prefix="/handlers", tags=["Datenhandler"])
router.include_router(outputs.router, prefix="/outputs", tags=["Ausgaben"])