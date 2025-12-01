from sqlalchemy import Column, Integer, DateTime, ForeignKey, UniqueConstraint
from datetime import datetime
from app.core.database import Base

class Favorite(Base):
    __tablename__ = "favorite"

    id = Column(Integer, primary_key=True, index=True)
    iduser = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    idanimal = Column(Integer, ForeignKey("animal.id", ondelete="CASCADE"), nullable=False)
    addeddate = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (UniqueConstraint('iduser', 'idanimal', name='_user_animal_uc'),)
