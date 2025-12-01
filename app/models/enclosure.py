from sqlalchemy import Column, Integer, String
from app.core.database import Base

class Enclosure(Base):
    __tablename__ = "enclosure"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    type = Column(String(100))
    capacity = Column(Integer)
    location = Column(String(255))
