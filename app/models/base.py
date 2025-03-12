from sqlalchemy import Column, Integer, DateTime, func
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import AsyncGenerator

from app.config.settings import settings

# Asynchrone Datenbank-Engine erstellen
engine = create_async_engine(settings.SQLITE_URL, echo=True)

# Sitzungsfactory erstellen
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

# Basisdefinition für SQLAlchemy-Modelle
Base = declarative_base()

# Basismodell mit allgemeinen Spalten
class BaseModel(Base):
    __abstract__ = True
    
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

async def init_db():
    """
    Initialisiert die Datenbank und erstellt Tabellen.
    """
    async with engine.begin() as conn:
        # Hier fügen wir keine Metadaten-Erstellung hinzu, das wird durch Alembic übernommen
        pass

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Erstellt und gibt eine neue Datenbanksitzung zurück.
    
    Returns:
        AsyncGenerator: Ein asynchroner Generator, der eine neue Datenbanksitzung liefert
    """
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()