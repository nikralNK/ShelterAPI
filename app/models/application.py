from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from datetime import datetime
from app.core.database import Base

class Application(Base):
    __tablename__ = "application"

    id = Column(Integer, primary_key=True, index=True)
    idanimal = Column(Integer, ForeignKey("animal.id", ondelete="CASCADE"), nullable=False)
    idguardian = Column(Integer, ForeignKey("guardian.id", ondelete="CASCADE"), nullable=False)
    applicationdate = Column(DateTime, default=datetime.utcnow)
    status = Column(String(50), default="На рассмотрении")
    comments = Column(Text)
