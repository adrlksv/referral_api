from sqlalchemy import Column, Integer, UUID, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

import uuid

from src.database import Base


class Referral(Base):
    __tablename__ = "referral"

    id = Column(Integer, primary_key=True)
    referral_code = Column(UUID(as_uuid=True), unique=True, default=uuid.uuid4)
    expiry_date = Column(TIMESTAMP(timezone=True), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)

    user = relationship("User", back_populates="referral_code")
