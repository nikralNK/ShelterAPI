from pydantic import BaseModel
from datetime import datetime

class FavoriteCreate(BaseModel):
    idanimal: int

class FavoriteResponse(BaseModel):
    id: int
    iduser: int
    idanimal: int
    addeddate: datetime

    class Config:
        from_attributes = True
