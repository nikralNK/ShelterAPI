from pydantic import BaseModel
from typing import Optional
from datetime import date

class AnimalBase(BaseModel):
    name: str
    type: Optional[str] = None
    breed: Optional[str] = None
    dateofbirth: Optional[date] = None
    gender: Optional[str] = None
    size: Optional[str] = None
    temperament: Optional[str] = None

class AnimalCreate(AnimalBase):
    idenclosure: Optional[int] = None

class AnimalUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None
    breed: Optional[str] = None
    dateofbirth: Optional[date] = None
    idenclosure: Optional[int] = None
    idguardian: Optional[int] = None
    currentstatus: Optional[str] = None
    gender: Optional[str] = None
    size: Optional[str] = None
    temperament: Optional[str] = None
    photo: Optional[str] = None

class AnimalResponse(AnimalBase):
    id: int
    idenclosure: Optional[int] = None
    idguardian: Optional[int] = None
    currentstatus: str
    photo: Optional[str] = None

    class Config:
        from_attributes = True
