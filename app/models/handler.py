from datetime import datetime
from typing import Optional

from pydantic import BaseModel, validator
from sqlalchemy import Column, String, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship

from app.models.base import BaseModel as SQLABaseModel

# SQLAlchemy-Modell
class Handler(SQLABaseModel):
    __tablename__ = "handlers"
    
    name = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    script = Column(Text, nullable=False)
    version = Column(Integer, nullable=False, default=1)
    
# Pydantic-Modelle für API-Validierung
class HandlerBase(BaseModel):
    name: str
    description: Optional[str] = None
    script: str
    
    @validator('script')
    def validate_script(cls, v):
        if not v.strip():
            raise ValueError("Das Skript darf nicht leer sein")
        return v
    
    class Config:
        orm_mode = True

class HandlerCreate(HandlerBase):
    pass

class HandlerUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    script: Optional[str] = None
    
    @validator('script')
    def validate_script(cls, v):
        if v is not None and not v.strip():
            raise ValueError("Das Skript darf nicht leer sein")
        return v
    
    class Config:
        orm_mode = True

class HandlerRead(HandlerBase):
    id: int
    version: int
    created_at: datetime
    updated_at: datetime