from fastapi import APIRouter, Depends, HTTPException
from fastapi_cache.decorator import cache

from datetime import datetime, timedelta

from time import sleep

import uuid

from src.referral.dao import ReferralDAO
from src.users.dao import UserDAO
from src.auth.jwt.dependencies import get_current_user
from src.referral.schemas import SCreateReferral
from src.users.models import User


router = APIRouter(
    prefix="/referral",
    tags=["Referral"]
)


@router.post("/create")
async def create_referral(
    data: SCreateReferral, current_user: User = Depends(get_current_user)
):
    existing_code = await ReferralDAO.find_one_or_none(user_id=current_user.id, is_active=True)
    if existing_code:
        raise HTTPException(status_code=400, detail="User already has an active referral code.")
    
    expiry_date = data.expiry_date if data.expiry_date else datetime.utcnow() + timedelta(days=30)
    referral = await ReferralDAO.add(
        referral_code=uuid.uuid4(),
        expiry_date=expiry_date,
        user_id=current_user.id,
        is_active=True
    )

    return referral


@router.delete("/delete")
async def delete_referral(current_user: User = Depends(get_current_user)):
    deleted = await ReferralDAO.delete_referral_code(current_user.id)
    if not deleted:
        raise HTTPException(status_code=404, detail="No active referral code found.")
    return {"message": "Referral code deleted successfully."}


@router.get("/code/{email}")
@cache(expire=3600)
async def get_referral_code(email: str):
    sleep(10)
    user = await UserDAO.find_one_or_none(email=email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    
    referral = await ReferralDAO.find_one_or_none(user_id=user.id, is_active=True)
    if not referral:
        raise HTTPException(status_code=404, detail="No active referral code found.")
    
    return referral


@router.post("/register/{referral_code}")
async def register_with_referral(referral_code: uuid.UUID, current_user: User = Depends(get_current_user)):
    referral = await ReferralDAO.find_one_or_none(referral_code=referral_code, is_active=True)
    if not referral:
        raise HTTPException(status_code=404, detail="Invalid or expired referral code.")
    
    await UserDAO.update(current_user.id, referrer_id=referral.user_id)

    return {
        "message": "Registered with referral code successfully."
    }


@router.get("/referrals")
@cache(expire=3600)
async def get_referrals(current_user: User = Depends(get_current_user)):
    sleep(10)
    referrals = await ReferralDAO.get_referrals(current_user.id)
    return referrals
