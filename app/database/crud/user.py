from datetime import datetime
from typing import Optional, List
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models import User, Subscription, SubscriptionStatus


async def get_user_by_telegram_id(db: AsyncSession, telegram_id: int) -> Optional[User]:
    result = await db.execute(select(User).where(User.telegram_id == telegram_id))
    return result.scalar_one_or_none()


async def get_user_by_id(db: AsyncSession, user_id: int) -> Optional[User]:
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()


async def create_user(
    db: AsyncSession,
    telegram_id: int,
    username: Optional[str] = None,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    language_code: str = "ru",
    referrer_id: Optional[int] = None
) -> User:
    user = User(
        telegram_id=telegram_id,
        username=username,
        first_name=first_name,
        last_name=last_name,
        language_code=language_code,
        referrer_id=referrer_id
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    
    subscription = Subscription(
        user_id=user.id,
        status=SubscriptionStatus.INACTIVE,
        daily_price=6.0
    )
    db.add(subscription)
    await db.commit()
    
    return user


async def update_user_balance(db: AsyncSession, user_id: int, amount: float) -> Optional[User]:
    user = await get_user_by_id(db, user_id)
    if user:
        user.balance += amount
        user.updated_at = datetime.utcnow()
        await db.commit()
        await db.refresh(user)
    return user


async def set_user_balance(db: AsyncSession, user_id: int, balance: float) -> Optional[User]:
    user = await get_user_by_id(db, user_id)
    if user:
        user.balance = balance
        user.updated_at = datetime.utcnow()
        await db.commit()
        await db.refresh(user)
    return user


async def update_user_remnawave(
    db: AsyncSession,
    user_id: int,
    remnawave_uuid: str,
    remnawave_short_uuid: str
) -> Optional[User]:
    user = await get_user_by_id(db, user_id)
    if user:
        user.remnawave_uuid = remnawave_uuid
        user.remnawave_short_uuid = remnawave_short_uuid
        user.updated_at = datetime.utcnow()
        await db.commit()
        await db.refresh(user)
    return user


async def get_all_users(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[User]:
    result = await db.execute(select(User).offset(skip).limit(limit))
    return result.scalars().all()


async def get_users_count(db: AsyncSession) -> int:
    result = await db.execute(select(User))
    return len(result.scalars().all())


async def mark_trial_used(db: AsyncSession, user_id: int) -> None:
    user = await get_user_by_id(db, user_id)
    if user:
        user.trial_used = True
        await db.commit()
