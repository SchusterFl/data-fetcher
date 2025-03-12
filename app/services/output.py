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
        result = await self.session.execute(