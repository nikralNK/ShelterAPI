from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ApplicationBase(BaseModel):
    idanimal: int
    idguardian: int
    comments: Optional[str] = None

class ApplicationCreate(ApplicationBase):
    pass

class ApplicationUpdate(BaseModel):
    status: Optional[str] = None
    comments: Optional[str] = None

class ApplicationResponse(ApplicationBase):
    id: int
    applicationdate: datetime
    status: str

    class Config:
        from_attributes = True
