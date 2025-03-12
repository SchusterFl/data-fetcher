import os
from datetime import datetime, timedelta
import httpx
from pathlib import Path
import asyncio
from loguru import logger

from app.config.settings import settings
from app.services.datasource import DataSourceService
from app.services.handler import HandlerService
from app.services.output import OutputService
from app.services.sandbox import SandboxService

async def fetch_and_process_data(datasource_id: int):
    """
    Abrufen und Verarbeiten von Daten aus einer Datenquelle.
    
    Args:
        datasource_id: ID der Datenquelle
    """
    try:
        # Services instanziieren
        datasource_service = DataSourceService()
        handler_service = HandlerService()
        output_service = OutputService()
        sandbox_service = SandboxService()
        
        # Datenquelle abrufen
        datasource = await datasource_service.get_by_id(datasource_id)
        if not datasource:
            logger.error(f"Datenquelle mit ID {datasource_id} nicht gefunden")
            return
        
        logger.info(f"Starte Datenabruf für Datenquelle '{datasource.name}' ({datasource.url})")
        
        # Daten abrufen
        async with httpx.AsyncClient() as client:
            response = await client.get(datasource.url)
            response.raise_for_status()
            data = response.text
        
        logger.info(f"Daten erfolgreich abgerufen von {datasource.url}")
        
        # Datenhandler und Ausgabekonfiguration abrufen
        # TODO: Implementiere die Verknüpfung zwischen Datenquellen, Handlern und Ausgaben
        # Annahme: Wir haben eine Methode, um die zugehörigen Handler und Ausgaben zu finden
        handlers = await handler_service.get_by_datasource(datasource_id)
        outputs = await output_service.get_by_datasource(datasource_id)
        
        # Daten verarbeiten und speichern
        for handler in handlers:
            try:
                # Daten im Sandbox-Kontext verarbeiten
                processed_data = await sandbox_service.execute_script(handler.script, data)
                
                # Für jede Ausgabekonfiguration speichern
                for output in outputs:
                    await output_service.save_data(processed_data, output)
                
                logger.info(f"Verarbeitung mit Handler '{handler.name}' erfolgreich abgeschlossen")
            except Exception as e:
                logger.error(f"Fehler bei der Verarbeitung mit Handler '{handler.name}': {str(e)}")
    
    except httpx.HTTPError as e:
        logger.error(f"HTTP-Fehler beim Abrufen der Daten: {str(e)}")
    except Exception as e:
        logger.error(f"Unerwarteter Fehler bei der Verarbeitung: {str(e)}")

async def cleanup_old_files():
    """
    Bereinigt alte Dateien basierend auf den Aufbewahrungsregeln.
    """
    try:
        output_service = OutputService()
        
        # Alle Ausgabekonfigurationen mit Zeitstempel-Strategie und Aufbewahrungsdauer abrufen
        outputs = await output_service.get_all_with_retention()
        
        for output in outputs:
            if not output.active:
                continue
                
            output_path = Path(output.path)
            if not output_path.exists() or not output_path.is_dir():
                logger.warning(f"Ausgabepfad '{output.path}' existiert nicht oder ist kein Verzeichnis")
                continue
            
            # Berechne das Datum, ab dem Dateien gelöscht werden sollen
            cutoff_date = datetime.now() - timedelta(days=output.retention_days)
            
            # Durchsuche Dateien im Ausgabeverzeichnis
            for file_path in output_path.glob("*"):
                if not file_path.is_file():
                    continue
                
                # Überprüfe die Dateierstellungszeit
                file_creation_time = datetime.fromtimestamp(file_path.stat().st_ctime)
                
                if file_creation_time < cutoff_date:
                    try:
                        os.remove(file_path)
                        logger.info(f"Alte Datei gelöscht: {file_path}")
                    except Exception as e:
                        logger.error(f"Fehler beim Löschen der Datei {file_path}: {str(e)}")
        
        logger.info("Bereinigung alter Dateien abgeschlossen")
    except Exception as e:
        logger.error(f"Fehler bei der Bereinigung alter Dateien: {str(e)}")