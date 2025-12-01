from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from app.core.database import Base

class Guardian(Base):
    __tablename__ = "guardian"

    id = Column(Integer, primary_key=True, index=True)
    fullname = Column(String(255), nullable=False)
    phonenumber = Column(String(50))
    email = Column(String(255))
    address = Column(Text)
    registrationdate = Column(DateTime, default=datetime.utcnow)
