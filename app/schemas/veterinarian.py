from pydantic import BaseModel
from typing import Optional

class VeterinarianBase(BaseModel):
    fullname: str
    specialization: Optional[str] = None
    phonenumber: Optional[str] = None
    licensenumber: Optional[str] = None

class VeterinarianCreate(VeterinarianBase):
    username: str
    password: str
    email: Optional[str] = None

class VeterinarianUpdate(BaseModel):
    fullname: Optional[str] = None
    specialization: Optional[str] = None
    phonenumber: Optional[str] = None
    licensenumber: Optional[str] = None

class VeterinarianResponse(VeterinarianBase):
    id: int
    iduser: Optional[int] = None

    class Config:
        from_attributes = True
