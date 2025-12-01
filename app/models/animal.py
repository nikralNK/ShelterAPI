from sqlalchemy import Column, Integer, String, Date, ForeignKey
from app.core.database import Base

class Animal(Base):
    __tablename__ = "animal"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    type = Column(String(100))
    breed = Column(String(100))
    dateofbirth = Column(Date)
    idenclosure = Column(Integer, ForeignKey("enclosure.id"))
    idguardian = Column(Integer, ForeignKey("guardian.id"))
    currentstatus = Column(String(50), default="Доступен")
    gender = Column(String(20))
    size = Column(String(50))
    temperament = Column(String(100))
    photo = Column(String(500))
