from datetime import datetime, timedelta
from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models import Subscription, SubscriptionStatus, User


async def get_subscription_by_user_id(db: AsyncSession, user_id: int) -> Optional[Subscription]:
    result = await db.execute(select(Subscription).where(Subscription.user_id == user_id))
    return result.scalar_one_or_none()


async def activate_subscription(
    db: AsyncSession,
    user_id: int,
    days: int = 1
) -> Optional[Subscription]:
    subscription = await get_subscription_by_user_id(db, user_id)
    if subscription:
        now = datetime.utcnow()
        if subscription.expires_at and subscription.expires_at > now:
            subscription.expires_at = subscription.expires_at + timedelta(days=days)
        else:
            subscription.expires_at = now + timedelta(days=days)
        
        subscription.status = SubscriptionStatus.ACTIVE
        subscription.days_paid += days
        subscription.last_charge_date = now
        subscription.updated_at = now
        
        await db.commit()
        await db.refresh(subscription)
    return subscription


async def deactivate_subscription(db: AsyncSession, user_id: int) -> Optional[Subscription]:
    subscription = await get_subscription_by_user_id(db, user_id)
    if subscription:
        subscription.status = SubscriptionStatus.INACTIVE
        subscription.updated_at = datetime.utcnow()
        await db.commit()
        await db.refresh(subscription)
    return subscription


async def get_active_subscriptions(db: AsyncSession) -> List[Subscription]:
    result = await db.execute(
        select(Subscription).where(Subscription.status == SubscriptionStatus.ACTIVE)
    )
    return result.scalars().all()


async def get_expired_subscriptions(db: AsyncSession) -> List[Subscription]:
    now = datetime.utcnow()
    result = await db.execute(
        select(Subscription).where(
            Subscription.status == SubscriptionStatus.ACTIVE,
            Subscription.expires_at < now
        )
    )
    return result.scalars().all()


async def set_trial_subscription(db: AsyncSession, user_id: int, days: int = 1) -> Optional[Subscription]:
    subscription = await get_subscription_by_user_id(db, user_id)
    if subscription:
        now = datetime.utcnow()
        subscription.status = SubscriptionStatus.TRIAL
        subscription.expires_at = now + timedelta(days=days)
        subscription.updated_at = now
        await db.commit()
        await db.refresh(subscription)
    return subscription
