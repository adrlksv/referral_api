from sqlalchemy import delete, update, select
from sqlalchemy.exc import NoResultFound
from datetime import datetime
import uuid

from src.dao.base import BaseDAO
from src.database import async_session_maker
from src.referral.models import Referral
from src.users.models import User


class ReferralDAO(BaseDAO):
    model = Referral

    @classmethod
    async def create_referral_code(cls, user_id: int, expiry_date: datetime):
        async with async_session_maker() as session:
            await session.execute(delete(Referral).where(Referral.user_id == user_id))
            
            referral_code = str(uuid.uuid4())
            new_referral = Referral(
                referral_code=referral_code,
                expiry_date=expiry_date,
                user_id=user_id,
                is_active=True
            )
            session.add(new_referral)
            await session.commit()
            return referral_code

    @classmethod
    async def get_referral_by_email(cls, email: str):
        async with async_session_maker() as session:
            result = await session.execute(
                select(Referral.referral_code)
                .join(User, Referral.user_id == User.id)
                .where(User.email == email, Referral.is_active)
            )
            return result.scalar_one_or_none()

    @classmethod
    async def delete_referral_code(cls, user_id: int):
        async with async_session_maker() as session:
            await session.execute(
                update(Referral)
                .where(Referral.user_id == user_id)
                .values(is_active=False)
            )
            await session.commit()

            return 200

    @classmethod
    async def register_with_referral(cls, user_id: int, referral_code: str):
        async with async_session_maker() as session:
            try:
                result = await session.execute(
                    select(Referral.user_id)
                    .where(Referral.referral_code == referral_code, Referral.is_active)
                )
                referrer_id = result.scalar_one()

                await session.execute(
                    update(User)
                    .where(User.id == user_id)
                    .values(referrer_id=referrer_id)
                )
                await session.commit()
                return referrer_id
            except NoResultFound:
                return None

    @classmethod
    async def get_referrals(cls, referrer_id: int):
        async with async_session_maker() as session:
            result = await session.execute(
                select(User.id, User.email, User.registration_date)
                .where(User.referrer_id == referrer_id)
            )
            return result.scalars().all()
