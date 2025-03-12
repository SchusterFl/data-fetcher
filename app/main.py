from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.api.routes import router as api_router
from app.config.settings import settings
from app.models.base import init_db
from app.utils.logging import setup_logging

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan-Event-Handler für FastAPI.
    """
    # Initialisierung bei App-Start
    setup_logging()
    await init_db()
    
    yield  # Warten, bis die App beendet wird
    
    # Cleanup oder weitere Shutdown-Logik könnte hier ergänzt werden

app = FastAPI(
    title="Data Fetch & Process Webapp",
    description="Eine interne Webapplikation zur Konfiguration und Verwaltung von Datenquellen, -verarbeitungen und -ausgaben",
    version="0.1.0",
    lifespan=lifespan,
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