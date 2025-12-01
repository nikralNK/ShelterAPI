from sqlalchemy import Column, Integer, String
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False, index=True)
    passwordhash = Column(String(255), nullable=False)
    email = Column(String(255))
    fullname = Column(String(255))
    role = Column(String(50), default="User")
    avatar = Column(String(500))
