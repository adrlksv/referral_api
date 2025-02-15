from sqlalchemy import Column, Integer, UUID, TIMESTAMP, ForeignKey, Boolean
from sqlalchemy.sql import func

import uuid

from src.database import Base


class Referral(Base):
    __tablename__ = "referral"

    id = Column(Integer, primary_key=True)
    referral_code = Column(UUID(as_uuid=True), unique=True, default=uuid.uuid4)
    expiry_date = Column(TIMESTAMP(timezone=True), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    is_active = Column(Boolean, default=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
