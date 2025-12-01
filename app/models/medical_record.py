from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from datetime import datetime
from app.core.database import Base

class MedicalRecord(Base):
    __tablename__ = "medical_record"

    id = Column(Integer, primary_key=True, index=True)
    idanimal = Column(Integer, ForeignKey("animal.id", ondelete="CASCADE"), nullable=False)
    idveterinarian = Column(Integer, ForeignKey("veterinarian.id"), nullable=False)
    visitdate = Column(DateTime, default=datetime.utcnow)
    diagnosis = Column(Text)
    treatment = Column(Text)
    notes = Column(Text)
