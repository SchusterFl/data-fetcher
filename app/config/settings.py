import os
from pathlib import Path
from typing import List

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """
    Anwendungskonfigurationseinstellungen, die aus Umgebungsvariablen geladen werden.
    """
    # Basisverzeichnis
    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent
    
    # API-Konfiguration
    API_V1_STR: str = "/v1"
    
    # CORS-Konfiguration
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8080"]
    
    # Datenbank-Konfiguration
    SQLITE_URL: str = f"sqlite+aiosqlite:///{BASE_DIR}/app.db"
    
    # Output-Konfiguration
    OUTPUT_DIR: Path = BASE_DIR / "output"
    
    # Logging-Konfiguration
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
    
    # Scheduler-Konfiguration
    SCHEDULER_MISFIRE_GRACE_TIME: int = 60  # Sekunden
    
    # Sandbox-Konfiguration
    SANDBOX_TIMEOUT: int = 30  # Sekunden
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

# Einstellungen-Instanz erstellen
settings = Settings()

# Stellen Sie sicher, dass OUTPUT_DIR existiert
os.makedirs(settings.OUTPUT_DIR, exist_ok=True)