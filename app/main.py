from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from app.api.routes import router as api_router
from app.config.settings import settings
from app.models.base import init_db
from app.utils.logging import setup_logging

app = FastAPI(
    title="Data Fetch & Process Webapp",
    description="Eine interne Webapplikation zur Konfiguration und Verwaltung von Datenquellen, -verarbeitungen und -ausgaben",
    version="0.1.0",
)

# CORS-Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Einbindung der API-Routen
app.include_router(api_router, prefix="/api")

# Health-Check-Endpunkt
@app.get("/health", tags=["Health"])
async def health_check():
    """
    Einfacher Health-Check-Endpunkt zur Überprüfung der API-Verfügbarkeit.
    """
    return {"status": "ok"}

@app.on_event("startup")
async def startup_event():
    """
    Ereignishandler für den Anwendungsstart.
    """
    # Initialisiert die Logging-Konfiguration
    setup_logging()
    
    # Initialisiert die Datenbank
    await init_db()

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)