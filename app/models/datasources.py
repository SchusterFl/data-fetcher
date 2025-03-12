from datetime import datetime, time
from typing import Optional

from pydantic import BaseModel, HttpUrl, validator
from sqlalchemy import Column, String, Integer, Time, Interval

from app.models.base import BaseModel as SQLABaseModel

# SQLAlchemy-Modell
class DataSource(SQLABaseModel):
    __tablename__ = "datasources"
    
    name = Column(String, index=True, nullable=False)
    url = Column(String, nullable=False)
    description = Column(String, nullable=True)
    start_time = Column(Time, nullable=False, default=time(0, 0))
    frequency = Column(Interval, nullable=False)
    
# Pydantic-Modelle für API-Validierung
class DataSourceBase(BaseModel):
    name: str
    url: HttpUrl
    description: Optional[str] = None
    start_time: time = time(0, 0)
    frequency: int  # Frequenz in Sekunden
    
    @validator('frequency')
    def validate_frequency(cls, v):
        if v <= 0:
            raise ValueError("Die Frequenz muss größer als 0 sein")
        return v
    
    class Config:
        orm_mode = True

class DataSourceCreate(DataSourceBase):
    pass

class DataSourceUpdate(BaseModel):
    name: Optional[str] = None
    url: Optional[HttpUrl] = None
    description: Optional[str] = None
    start_time: Optional[time] = None
    frequency: Optional[int] = None
    
    @validator('frequency')
    def validate_frequency(cls, v):
        if v is not None and v <= 0:
            raise ValueError("Die Frequenz muss größer als 0 sein")
        return v
    
    class Config:
        orm_mode = True

class DataSourceRead(DataSourceBase):
    id: int
    created_at: datetime
    updated_at: datetime