"""
Dienst für die Verwaltung von Datenhandlern.
"""

from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional, Dict, Any

from app.models.base import get_session
from app.models.handler import Handler, HandlerCreate, HandlerUpdate
from app.services.sandbox import SandboxService

class HandlerService:
    """
    Service-Klasse für die Verwaltung von Datenhandlern.
    """
    
    def __init__(
        self, 
        session: AsyncSession = Depends(get_session),
        sandbox_service: SandboxService = Depends()
    ):
        self.session = session
        self.sandbox_service = sandbox_service
    
    async def create(self, handler: HandlerCreate) -> Handler:
        """
        Erstellt einen neuen Datenhandler.
        
        Args:
            handler: Der zu erstellende Datenhandler
            
        Returns:
            Handler: Der erstellte Datenhandler
        """
        # Handler erstellen
        db_handler = Handler(
            name=handler.name,
            description=handler.description,
            script=handler.script,
            version=1
        )
        
        self.session.add(db_handler)
        await self.session.commit()
        await self.session.refresh(db_handler)
        
        return db_handler
    
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Handler]:
        """
        Gibt alle Datenhandler zurück.
        
        Args:
            skip: Anzahl der zu überspringenden Datensätze
            limit: Maximale Anzahl der zurückzugebenden Datensätze
            
        Returns:
            List[Handler]: Liste von Datenhandlern
        """
        query = select(Handler).offset(skip).limit(limit)
        result = await self.session.execute(query)
        return result.scalars().all()
    
    async def get_by_id(self, handler_id: int) -> Optional[Handler]:
        """
        Gibt einen Datenhandler anhand seiner ID zurück.
        
        Args:
            handler_id: ID des gesuchten Datenhandlers
            
        Returns:
            Optional[Handler]: Der gefundene Datenhandler oder None
        """
        query = select(Handler).where(Handler.id == handler_id)
        result = await self.session.execute(query)
        return result.scalars().first()
    
    async def update(self, handler_id: int, handler_update: HandlerUpdate) -> Handler:
        """
        Aktualisiert einen vorhandenen Datenhandler.
        
        Args:
            handler_id: ID des zu aktualisierenden Datenhandlers
            handler_update: Die Aktualisierungsdaten
            
        Returns:
            Handler: Der aktualisierte Datenhandler
        """
        db_handler = await self.get_by_id(handler_id)
        if db_handler is None:
            raise HTTPException(status_code=404, detail="Datenhandler nicht gefunden")
        
        # Aktualisierbare Felder
        update_data = handler_update.dict(exclude_unset=True)
        
        # Wenn das Skript geändert wird, erhöhen wir die Version
        if "script" in update_data and update_data["script"] != db_handler.script:
            db_handler.version += 1
        
        # Update durchführen
        for key, value in update_data.items():
            setattr(db_handler, key, value)
        
        await self.session.commit()
        await self.session.refresh(db_handler)
        
        return db_handler
    
    async def delete(self, handler_id: int) -> None:
        """
        Löscht einen Datenhandler.
        
        Args:
            handler_id: ID des zu löschenden Datenhandlers
        """
        db_handler = await self.get_by_id(handler_id)
        if db_handler is None:
            raise HTTPException(status_code=404, detail="Datenhandler nicht gefunden")
        
        await self.session.delete(db_handler)
        await self.session.commit()
    
    async def test_handler(self, handler: Handler, test_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Testet einen Datenhandler mit Testdaten.
        
        Args:
            handler: Der zu testende Datenhandler
            test_data: Die Testdaten
            
        Returns:
            Dict[str, Any]: Die Ergebnisse der Testausführung
        """
        # Sandbox-Service nutzen, um den Handler mit Testdaten auszuführen
        return await self.sandbox_service.execute_script(handler.script, test_data)
    
    async def execute_handler(self, handler: Handler, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Führt einen Datenhandler mit Daten aus.
        
        Args:
            handler: Der auszuführende Datenhandler
            data: Die zu verarbeitenden Daten
            
        Returns:
            Dict[str, Any]: Die Ergebnisse der Ausführung
        """
        # Sandbox-Service nutzen, um den Handler mit den Daten auszuführen
        return await self.sandbox_service.execute_script(handler.script, data)