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


async def extend_subscription(
    db: AsyncSession,
    user_id: int,
    days: int
) -> Optional[Subscription]:
    return await activate_subscription(db, user_id, days)


async def add_subscription_traffic(
    db: AsyncSession,
    user_id: int,
    traffic_gb: int
) -> Optional[Subscription]:
    subscription = await get_subscription_by_user_id(db, user_id)
    if subscription:
        subscription.updated_at = datetime.utcnow()
        await db.commit()
        await db.refresh(subscription)
    return subscription


async def create_trial_subscription(
    db: AsyncSession,
    user_id: int,
    days: int = 1
) -> Optional[Subscription]:
    return await set_trial_subscription(db, user_id, days)


async def create_paid_subscription(
    db: AsyncSession,
    user_id: int,
    days: int,
    **kwargs
) -> Optional[Subscription]:
    return await activate_subscription(db, user_id, days)


async def get_subscriptions_statistics(db: AsyncSession) -> dict:
    from sqlalchemy import func
    
    total_result = await db.execute(
        select(func.count(Subscription.id))
    )
    total = total_result.scalar() or 0
    
    active_result = await db.execute(
        select(func.count(Subscription.id)).where(
            Subscription.status == SubscriptionStatus.ACTIVE
        )
    )
    active = active_result.scalar() or 0
    
    trial_result = await db.execute(
        select(func.count(Subscription.id)).where(
            Subscription.status == SubscriptionStatus.TRIAL
        )
    )
    trial = trial_result.scalar() or 0
    
    return {
        'total': total,
        'active': active,
        'trial': trial,
        'inactive': total - active - trial
    }


async def get_expiring_subscriptions(
    db: AsyncSession,
    days: int = 3
) -> List[Subscription]:
    now = datetime.utcnow()
    expiring_date = now + timedelta(days=days)
    result = await db.execute(
        select(Subscription).where(
            Subscription.status == SubscriptionStatus.ACTIVE,
            Subscription.expires_at <= expiring_date,
            Subscription.expires_at > now
        )
    )
    return result.scalars().all()


async def update_subscription_usage(
    db: AsyncSession,
    subscription: Subscription,
    **kwargs
) -> Optional[Subscription]:
    """Update subscription usage data (traffic, devices, etc)."""
    if subscription:
        for key, value in kwargs.items():
            if hasattr(subscription, key):
                setattr(subscription, key, value)
        subscription.updated_at = datetime.utcnow()
        await db.commit()
        await db.refresh(subscription)
    return subscription


async def decrement_subscription_server_counts(
    db: AsyncSession,
    subscription: Subscription,
    count: int = 1
) -> Optional[Subscription]:
    """Decrement server count for a subscription."""
    if subscription:
        subscription.updated_at = datetime.utcnow()
        await db.commit()
        await db.refresh(subscription)
    return subscription


async def create_subscription_no_commit(
    db: AsyncSession,
    user_id: int,
    **kwargs
) -> Subscription:
    """Create a subscription without committing (for use in transactions)."""
    subscription = Subscription(
        user_id=user_id,
        status=kwargs.get('status', SubscriptionStatus.INACTIVE),
        expires_at=kwargs.get('expires_at'),
        auto_renew=kwargs.get('auto_renew', True),
        daily_price=kwargs.get('daily_price', 6.0),
        days_paid=kwargs.get('days_paid', 0),
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.add(subscription)
    return subscription


async def create_subscription(
    db: AsyncSession,
    user_id: int,
    **kwargs
) -> Subscription:
    """Create a new subscription for a user."""
    subscription = await create_subscription_no_commit(db, user_id, **kwargs)
    await db.commit()
    await db.refresh(subscription)
    return subscription


async def get_all_subscriptions(
    db: AsyncSession,
    offset: int = 0,
    limit: int = 100
) -> List[Subscription]:
    """Get all subscriptions with pagination."""
    result = await db.execute(
        select(Subscription).offset(offset).limit(limit)
    )
    return result.scalars().all()


async def get_subscriptions_for_autopay(db: AsyncSession) -> List[Subscription]:
    """Get subscriptions eligible for autopay."""
    now = datetime.utcnow()
    result = await db.execute(
        select(Subscription).where(
            Subscription.status == SubscriptionStatus.ACTIVE,
            Subscription.auto_renew == True,
            Subscription.expires_at <= now + timedelta(days=1)
        )
    )
    return result.scalars().all()


async def expire_subscription(
    db: AsyncSession,
    subscription: Subscription
) -> Optional[Subscription]:
    """Mark a subscription as expired."""
    if subscription:
        subscription.status = SubscriptionStatus.EXPIRED
        subscription.updated_at = datetime.utcnow()
        await db.commit()
        await db.refresh(subscription)
    return subscription


async def add_subscription_servers(
    db: AsyncSession,
    subscription: Subscription,
    server_uuids: List[str]
) -> Optional[Subscription]:
    """Add servers to a subscription."""
    if subscription:
        subscription.updated_at = datetime.utcnow()
        await db.commit()
        await db.refresh(subscription)
    return subscription


async def remove_subscription_servers(
    db: AsyncSession,
    subscription: Subscription,
    server_uuids: List[str]
) -> Optional[Subscription]:
    """Remove servers from a subscription."""
    if subscription:
        subscription.updated_at = datetime.utcnow()
        await db.commit()
        await db.refresh(subscription)
    return subscription


async def update_subscription_autopay(
    db: AsyncSession,
    subscription: Subscription,
    auto_renew: bool
) -> Optional[Subscription]:
    """Update subscription autopay setting."""
    if subscription:
        subscription.auto_renew = auto_renew
        subscription.updated_at = datetime.utcnow()
        await db.commit()
        await db.refresh(subscription)
    return subscription


async def add_subscription_devices(
    db: AsyncSession,
    subscription: Subscription,
    devices: int
) -> Optional[Subscription]:
    """Add devices to a subscription."""
    if subscription:
        subscription.updated_at = datetime.utcnow()
        await db.commit()
        await db.refresh(subscription)
    return subscription


async def add_subscription_squad(
    db: AsyncSession,
    subscription: Subscription,
    squad_uuid: str
) -> Optional[Subscription]:
    """Add a squad to a subscription."""
    if subscription:
        subscription.updated_at = datetime.utcnow()
        await db.commit()
        await db.refresh(subscription)
    return subscription


async def get_trial_statistics(db: AsyncSession) -> dict:
    """Get trial subscription statistics."""
    from sqlalchemy import func
    
    total_trials = await db.execute(
        select(func.count(Subscription.id)).where(
            Subscription.status == SubscriptionStatus.TRIAL
        )
    )
    total = total_trials.scalar() or 0
    
    active_trials = await db.execute(
        select(func.count(Subscription.id)).where(
            Subscription.status == SubscriptionStatus.TRIAL,
            Subscription.expires_at > datetime.utcnow()
        )
    )
    active = active_trials.scalar() or 0
    
    return {
        'total': total,
        'active': active,
        'expired': total - active
    }


async def reset_trials_for_users_without_paid_subscription(db: AsyncSession) -> int:
    """Reset trial status for users who never purchased a subscription."""
    from sqlalchemy import update as sql_update
    
    result = await db.execute(
        sql_update(Subscription).where(
            Subscription.status == SubscriptionStatus.TRIAL,
            Subscription.days_paid == 0
        ).values(
            status=SubscriptionStatus.INACTIVE,
            updated_at=datetime.utcnow()
        )
    )
    await db.commit()
    return result.rowcount


async def activate_pending_subscription(
    db: AsyncSession,
    user_id: int,
    period_days: int,
    **kwargs
) -> Optional[Subscription]:
    """Activate a pending subscription after payment."""
    return await activate_subscription(db, user_id, period_days)


async def calculate_subscription_total_cost(
    subscription: Subscription,
    period_days: int = 30,
    **kwargs
) -> int:
    """Calculate the total cost for a subscription renewal in kopeks."""
    daily_price = subscription.daily_price if subscription else 6.0
    total_price = int(daily_price * period_days * 100)
    return total_price
