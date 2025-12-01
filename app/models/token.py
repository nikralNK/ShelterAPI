from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from datetime import datetime
from app.core.database import Base

class Token(Base):
    __tablename__ = "tokens"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String(500), unique=True, nullable=False, index=True)
    iduser = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    createdat = Column(DateTime, default=datetime.utcnow)
    expiresat = Column(DateTime, nullable=False)
    isrevoked = Column(Boolean, default=False)
