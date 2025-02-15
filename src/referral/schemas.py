from pydantic import BaseModel, UUID4

from datetime import datetime


class SCreateReferral(BaseModel):
    expiry_date: datetime


class SReferralResponse(BaseModel):
    id: int
    referral_code: UUID4
    expiry_date: datetime
    create_at: datetime
    is_active: bool
    user_id: int

    class Config:
        from_attributes = True
