from sqlalchemy import Column, Integer, String, ForeignKey
from app.core.database import Base

class Veterinarian(Base):
    __tablename__ = "veterinarian"

    id = Column(Integer, primary_key=True, index=True)
    fullname = Column(String(255), nullable=False)
    specialization = Column(String(100))
    phonenumber = Column(String(50))
    licensenumber = Column(String(100))
    iduser = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
