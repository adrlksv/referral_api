from sqlalchemy import TIMESTAMP, Column, Integer, String, ForeignKey
from sqlalchemy.sql import func

from src.database import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    email = Column(String(255), nullable=False, unique=True)
    login = Column(String(255), nullable=False)
    hashed_password = Column(String, nullable=False)
    referrer_id = Column(Integer, ForeignKey("user.id"), nullable=True)

    registration_date = Column(TIMESTAMP(timezone=True), server_default=func.now())
