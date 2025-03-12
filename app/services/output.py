"""
Dienst für die Verwaltung von Ausgabekonfigurationen.
"""

import os
import aiofiles
from datetime import datetime
from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional, Dict, Any, BinaryIO

from app.models.base import get_session
from app.models.output import Output, OutputCreate, OutputUpdate, OutputStrategy
from app.config.settings import settings

class OutputService:
    """
    Service-Klasse für die Verwaltung von Ausgabekonfigurationen.
    """
    
    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.session = session
        self.base_output_dir = settings.OUTPUT_DIR
    
    async def create(self, output: OutputCreate) -> Output:
        """
        Erstellt eine neue Ausgabekonfiguration.
        
        Args:
            output: Die zu erstellende Ausgabekonfiguration
            
        Returns:
            Output: Die erstellte Ausgabekonfiguration
        """
        # Ausgabekonfiguration erstellen
        db_output = Output(
            name=output.name,
            description=output.description,
            path=output.path,
            strategy=output.strategy,
            retention_days=output.retention_days,
            active=output.active
        )
        
        self.session.add(db_output)
        await self.session.commit()
        await self.session.refresh(db_output)
        
        # Zielverzeichnis erstellen, falls es nicht existiert
        output_dir = os.path.join(self.base_output_dir, os.path.dirname(output.path))
        os.makedirs(output_dir, exist_ok=True)
        
        return db_output
    
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Output]:
        """
        Gibt alle Ausgabekonfigurationen zurück.
        
        Args:
            skip: Anzahl der zu überspringenden Datensätze
            limit: Maximale Anzahl der zurückzugebenden Datensätze
            
        Returns:
            List[Output]: Liste von Ausgabekonfigurationen
        """
        query = select(Output).offset(skip).limit(limit)
        result = await self.session.execute(query)
        return result.scalars().all()
    
    async def get_by_id(self, output_id: int) -> Optional[Output]:
        """
        Gibt eine Ausgabekonfiguration anhand ihrer ID zurück.
        
        Args:
            output_id: ID der gesuchten Ausgabekonfiguration
            
        Returns:
            Optional[Output]: Die gefundene Ausgabekonfiguration oder None
        """
        query = select(Output).where(Output.id == output_id)
        result = await self.session.execute(query)
        return result.scalars().first()
    
    async def update(self, output_id: int, output_update: OutputUpdate) -> Output:
        """
        Aktualisiert eine Ausgabekonfiguration.
        
        Args:
            output_id: ID der zu aktualisierenden Ausgabekonfiguration
            output_update: Die zu aktualisierenden Daten
            
        Returns:
            Output: Die aktualisierte Ausgabekonfiguration
        """
        db_output = await self.get_by_id(output_id)
        if not db_output:
            raise HTTPException(status_code=404, detail="Ausgabekonfiguration nicht gefunden")
        
        # Aktualisierung der Felder
        update_data = output_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_output, key, value)
        
        await self.session.commit()
        await self.session.refresh(db_output)
        
        # Wenn der Pfad geändert wurde, erstelle den neuen Ordner
        if 'path' in update_data:
            output_dir = os.path.join(self.base_output_dir, os.path.dirname(db_output.path))
            os.makedirs(output_dir, exist_ok=True)
        
        return db_output
    
    async def delete(self, output_id: int) -> None:
        """
        Löscht eine Ausgabekonfiguration.
        
        Args:
            output_id: ID der zu löschenden Ausgabekonfiguration
        """
        db_output = await self.get_by_id(output_id)
        if not db_output:
            raise HTTPException(status_code=404, detail="Ausgabekonfiguration nicht gefunden")
        
        await self.session.delete(db_output)
        await self.session.commit()
    
    async def write_data_to_output(self, output_id: int, data: bytes) -> str:
        """
        Schreibt Daten in eine Ausgabekonfiguration.
        
        Args:
            output_id: ID der Ausgabekonfiguration
            data: Zu schreibende Daten
            
        Returns:
            str: Pfad zur geschriebenen Datei
        """
        db_output = await self.get_by_id(output_id)
        if not db_output:
            raise HTTPException(status_code=404, detail="Ausgabekonfiguration nicht gefunden")
        
        # Vollständigen Pfad erstellen
        full_path = os.path.join(self.base_output_dir, db_output.path)
        
        # Pfad mit Zeitstempel für die Strategie TIMESTAMP
        if db_output.strategy == OutputStrategy.TIMESTAMP:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename, extension = os.path.splitext(full_path)
            full_path = f"{filename}_{timestamp}{extension}"
        
        # Verzeichnis erstellen, falls es nicht existiert
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        
        # Daten in die Datei schreiben
        async with aiofiles.open(full_path, 'wb') as file:
            await file.write(data)
        
        return full_path
    
    async def clean_old_files(self, output_id: int) -> int:
        """
        Löscht alte Dateien basierend auf der Aufbewahrungsdauer.
        Diese Funktion sollte regelmäßig für alle Ausgaben mit TIMESTAMP-Strategie aufgerufen werden.
        
        Args:
            output_id: ID der Ausgabekonfiguration
            
        Returns:
            int: Anzahl der gelöschten Dateien
        """
        db_output = await self.get_by_id(output_id)
        if not db_output:
            raise HTTPException(status_code=404, detail="Ausgabekonfiguration nicht gefunden")
        
        # Nur für Ausgaben mit TIMESTAMP-Strategie und definierter Aufbewahrungsdauer
        if db_output.strategy != OutputStrategy.TIMESTAMP or not db_output.retention_days:
            return 0
        
        # Verzeichnis und Basisnamen der Dateien bestimmen
        output_dir = os.path.dirname(os.path.join(self.base_output_dir, db_output.path))
        base_filename = os.path.basename(db_output.path)
        filename, extension = os.path.splitext(base_filename)
        
        # Alle Dateien im Verzeichnis durchgehen
        deleted_count = 0
        now = datetime.now()
        
        for file in os.listdir(output_dir):
            if file.startswith(filename) and file.endswith(extension) and "_" in file:
                # Extrahiere den Zeitstempel aus dem Dateinamen
                try:
                    timestamp_str = file.replace(filename + "_", "").replace(extension, "")
                    file_timestamp = datetime.strptime(timestamp_str, "%Y%m%d_%H%M%S")
                    
                    # Berechne das Alter der Datei in Tagen
                    age_days = (now - file_timestamp).days
                    
                    # Lösche Dateien, die älter als die Aufbewahrungsdauer sind
                    if age_days > db_output.retention_days:
                        file_path = os.path.join(output_dir, file)
                        os.remove(file_path)
                        deleted_count += 1
                except (ValueError, Exception):
                    # Bei Fehlern (z.B. unpassender Dateiname) überspringen
                    continue
        
        return deleted_count