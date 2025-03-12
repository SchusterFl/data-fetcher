import logging
import sys
from pathlib import Path

from loguru import logger

from app.config.settings import settings

class InterceptHandler(logging.Handler):
    """
    Handler für die Weiterleitung von Standardloggingmeldungen an Loguru.
    """
    def emit(self, record):
        # Entsprechende Loguru-Level-Methode abrufen
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Pfad des Aufrufers ermitteln
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())

def setup_logging():
    """
    Konfiguriert das Logging für die Anwendung.
    """
    # Loguru-Konfiguration
    log_file_path = Path(settings.BASE_DIR) / "logs" / "app.log"
    log_file_path.parent.mkdir(parents=True, exist_ok=True)

    logger.configure(
        handlers=[
            {"sink": sys.stdout, "format": settings.LOG_FORMAT, "level": settings.LOG_LEVEL},
            {
                "sink": str(log_file_path),
                "format": settings.LOG_FORMAT,
                "level": settings.LOG_LEVEL,
                "rotation": "10 MB",
                "retention": "1 week",
                "compression": "zip",
            },
        ],
    )

    # Standard-Logging-Handler abfangen
    logging.basicConfig(handlers=[InterceptHandler()], level=0)
    
    # Module, die umgeleitet werden sollen
    modules = [
        "uvicorn",
        "uvicorn.error",
        "uvicorn.access",
        "fastapi",
        "sqlalchemy",
        "apscheduler",
    ]
    
    for module in modules:
        logging.getLogger(module).handlers = [InterceptHandler()]

    # Loguru als Standardlogger verwenden
    logger.info("Logging wurde eingerichtet")