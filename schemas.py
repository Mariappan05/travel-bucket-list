from pydantic import BaseModel
from typing import Optional

class DestinationBase(BaseModel):
    place_name: str
    country: str
    priority: str
    notes: Optional[str] = None

class DestinationCreate(DestinationBase):
    pass

class DestinationUpdate(BaseModel):
    place_name: Optional[str] = None
    country: Optional[str] = None
    priority: Optional[str] = None
    notes: Optional[str] = None
    visited: Optional[bool] = None

class Destination(DestinationBase):
    id: int
    visited: bool
    
    class Config:
        orm_mode = True