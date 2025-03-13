"""
Dienst für die Verwaltung von Datenquellen.
"""

from datetime import timedelta
from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from app.models.base import get_session
from app.models.datasource import DataSource, DataSourceCreate, DataSourceUpdate
from app.utils.validators import validate_url

class DataSourceService:
    """
    Service-Klasse für die Verwaltung von Datenquellen.
    """
    
    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.session = session
    
    async def create(self, datasource: DataSourceCreate) -> DataSource:
        """
        Erstellt eine neue Datenquelle.
        
        Args:
            datasource: Die zu erstellende Datenquelle
            
        Returns:
            DataSource: Die erstellte Datenquelle
        """
        # URL validieren
        await validate_url(str(datasource.url))
        
        # Datenquelle erstellen
        db_datasource = DataSource(
            name=datasource.name,
            url=str(datasource.url),
            description=datasource.description,
            start_time=datasource.start_time,
            frequency=timedelta(seconds=datasource.frequency)
        )
        
        self.session.add(db_datasource)
        await self.session.commit()
        await self.session.refresh(db_datasource)
        
        return db_datasource
    
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[DataSource]:
        """
        Gibt alle Datenquellen zurück.
        
        Args:
            skip: Anzahl der zu überspringenden Datensätze
            limit: Maximale Anzahl der zurückzugebenden Datensätze
            
        Returns:
            List[DataSource]: Liste von Datenquellen
        """
        query = select(DataSource).offset(skip).limit(limit)
        result = await self.session.execute(query)
        return result.scalars().all()
    
    async def get_by_id(self, datasource_id: int) -> Optional[DataSource]:
        """
        Gibt eine Datenquelle anhand ihrer ID zurück.
        
        Args:
            datasource_id: ID der gesuchten Datenquelle
            
        Returns:
            Optional[DataSource]: Die gefundene Datenquelle oder None
        """
        query = select(DataSource).where(DataSource.id == datasource_id)
        result = await self.session.execute(query)
        return result.scalars().first()
    
    async def update(self, datasource_id: int, datasource_update: DataSourceUpdate) -> DataSource:
        """
        Aktualisiert eine vorhandene Datenquelle.
        
        Args:
            datasource_id: ID der zu aktualisierenden Datenquelle
            datasource_update: Die Aktualisierungsdaten
            
        Returns:
            DataSource: Die aktualisierte Datenquelle
        """
        db_datasource = await self.get_by_id(datasource_id)
        if db_datasource is None:
            raise HTTPException(status_code=404, detail="Datenquelle nicht gefunden")
        
        # Aktualisierbare Felder
        update_data = datasource_update.model_dump(exclude_unset=True)
        
        # URL validieren, falls eine neue angegeben wurde
        if "url" in update_data:
            await validate_url(str(update_data["url"]))
            update_data["url"] = str(update_data["url"])
        
        # Frequenz in Timedelta umwandeln, falls angegeben
        if "frequency" in update_data:
            update_data["frequency"] = timedelta(seconds=update_data["frequency"])
        
        # Update durchführen
        for key, value in update_data.items():
            setattr(db_datasource, key, value)
        
        await self.session.commit()
        await self.session.refresh(db_datasource)
        
        return db_datasource

    async def delete(self, datasource_id: int) -> None:
        """
        Löscht eine Datenquelle.
        
        Args:
            datasource_id: ID der zu löschenden Datenquelle
        """
        db_datasource = await self.get_by_id(datasource_id)
        if db_datasource is None:
            raise HTTPException(status_code=404, detail="Datenquelle nicht gefunden")
        
        await self.session.delete(db_datasource)
        await self.session.commit()