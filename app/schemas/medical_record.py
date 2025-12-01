from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class MedicalRecordBase(BaseModel):
    idanimal: int
    diagnosis: Optional[str] = None
    treatment: Optional[str] = None
    notes: Optional[str] = None

class MedicalRecordCreate(MedicalRecordBase):
    pass

class MedicalRecordUpdate(BaseModel):
    diagnosis: Optional[str] = None
    treatment: Optional[str] = None
    notes: Optional[str] = None

class MedicalRecordResponse(MedicalRecordBase):
    id: int
    idveterinarian: int
    visitdate: datetime

    class Config:
        from_attributes = True
