from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, validator
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.models.base import BaseModel as SQLABaseModel

# Enum für Ausgabestrategien
class OutputStrategy(str, Enum):
    OVERWRITE = "overwrite"
    TIMESTAMP = "timestamp"

# SQLAlchemy-Modell
class Output(SQLABaseModel):
    __tablename__ = "outputs"
    
    name = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    path = Column(String, nullable=False)
    strategy = Column(String, nullable=False, default=OutputStrategy.OVERWRITE)
    retention_days = Column(Integer, nullable=True)  # Aufbewahrungsdauer in Tagen (nur für timestamp-Strategie)
    active = Column(Boolean, nullable=False, default=True)
    
# Pydantic-Modelle für API-Validierung
class OutputBase(BaseModel):
    name: str
    description: Optional[str] = None
    path: str
    strategy: OutputStrategy = OutputStrategy.OVERWRITE
    retention_days: Optional[int] = None
    active: bool = True
    
    @validator('retention_days')
    def validate_retention_days(cls, v, values):
        if v is not None:
            if v <= 0:
                raise ValueError("Die Aufbewahrungsdauer muss größer als 0 sein")
            
            # Wenn Strategie OVERWRITE ist, sollte keine Aufbewahrungsdauer angegeben werden
            if values.get('strategy') == OutputStrategy.OVERWRITE:
                raise ValueError("Bei der 'overwrite'-Strategie kann keine Aufbewahrungsdauer festgelegt werden")
        elif values.get('strategy') == OutputStrategy.TIMESTAMP:
            # Bei TIMESTAMP-Strategie muss eine Aufbewahrungsdauer angegeben werden
            raise ValueError("Bei der 'timestamp'-Strategie muss eine Aufbewahrungsdauer festgelegt werden")
        
        return v
    
    class Config:
        orm_mode = True

class OutputCreate(OutputBase):
    pass

class OutputUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    path: Optional[str] = None
    strategy: Optional[OutputStrategy] = None
    retention_days: Optional[int] = None
    active: Optional[bool] = None
    
    @validator('retention_days')
    def validate_retention_days(cls, v, values):
        if v is not None:
            if v <= 0:
                raise ValueError("Die Aufbewahrungsdauer muss größer als 0 sein")
            
            # Wenn Strategie OVERWRITE ist, sollte keine Aufbewahrungsdauer angegeben werden
            if values.get('strategy') == OutputStrategy.OVERWRITE:
                raise ValueError("Bei der 'overwrite'-Strategie kann keine Aufbewahrungsdauer festgelegt werden")
        elif values.get('strategy') == OutputStrategy.TIMESTAMP:
            # Bei TIMESTAMP-Strategie muss eine Aufbewahrungsdauer angegeben werden
            raise ValueError("Bei der 'timestamp'-Strategie muss eine Aufbewahrungsdauer festgelegt werden")
        
        return v
    
    class Config:
        orm_mode = True

class OutputRead(OutputBase):
    id: int
    created_at: datetime
    updated_at: datetime