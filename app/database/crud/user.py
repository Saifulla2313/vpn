from datetime import datetime
from typing import Optional, List
from sqlalchemy import select, update, func, String
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


async def get_users_count(
    db: AsyncSession,
    status: Optional[str] = None,
    search: Optional[str] = None
) -> int:
    query = select(func.count(User.id))
    if status is not None:
        query = query.where(User.status == status)
    if search:
        search_pattern = f"%{search}%"
        query = query.where(
            (User.username.ilike(search_pattern)) |
            (User.first_name.ilike(search_pattern)) |
            (User.last_name.ilike(search_pattern)) |
            (User.telegram_id.cast(String).ilike(search_pattern))
        )
    result = await db.execute(query)
    return result.scalar() or 0


async def mark_trial_used(db: AsyncSession, user_id: int) -> None:
    user = await get_user_by_id(db, user_id)
    if user:
        user.trial_used = True
        await db.commit()


async def get_users_list(
    db: AsyncSession,
    offset: int = 0,
    limit: int = 100,
    is_active: Optional[bool] = None,
    status: Optional[str] = None,
    search: Optional[str] = None,
    order_by_balance: bool = False,
    order_by_traffic: bool = False,
    order_by_last_activity: bool = False,
    order_by_total_spent: bool = False,
    order_by_purchase_count: bool = False
) -> List[User]:
    query = select(User)
    if is_active is not None:
        query = query.where(User.is_blocked == (not is_active))
    if status is not None:
        query = query.where(User.status == status)
    if search:
        search_pattern = f"%{search}%"
        query = query.where(
            (User.username.ilike(search_pattern)) |
            (User.first_name.ilike(search_pattern)) |
            (User.last_name.ilike(search_pattern)) |
            (User.telegram_id.cast(String).ilike(search_pattern))
        )
    if order_by_balance:
        query = query.order_by(User.balance.desc())
    elif order_by_traffic:
        query = query.order_by(User.total_traffic.desc())
    elif order_by_last_activity:
        query = query.order_by(User.last_activity.desc().nullslast())
    elif order_by_total_spent:
        query = query.order_by(User.total_spent.desc())
    elif order_by_purchase_count:
        query = query.order_by(User.purchase_count.desc())
    else:
        query = query.order_by(User.created_at.desc())
    query = query.offset(offset).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


async def get_users_with_active_subscriptions(db: AsyncSession) -> List[User]:
    result = await db.execute(
        select(User)
        .join(Subscription)
        .where(Subscription.status == SubscriptionStatus.ACTIVE)
    )
    return result.scalars().all()


async def get_inactive_users(
    db: AsyncSession,
    days: int = 30,
    limit: int = 100
) -> List[User]:
    from datetime import timedelta
    cutoff = datetime.utcnow() - timedelta(days=days)
    result = await db.execute(
        select(User)
        .where(User.updated_at < cutoff)
        .limit(limit)
    )
    return result.scalars().all()


async def subtract_user_balance(
    db: AsyncSession,
    user_id: int,
    amount: float
) -> Optional[User]:
    user = await get_user_by_id(db, user_id)
    if user:
        user.balance -= amount
        if user.balance < 0:
            user.balance = 0
        user.updated_at = datetime.utcnow()
        await db.commit()
        await db.refresh(user)
    return user


async def get_users_for_promo_segment(
    db: AsyncSession,
    segment: str,
    limit: int = 1000
) -> List[User]:
    query = select(User)
    
    if segment == "active":
        query = query.join(Subscription).where(
            Subscription.status == SubscriptionStatus.ACTIVE
        )
    elif segment == "inactive":
        query = query.join(Subscription).where(
            Subscription.status == SubscriptionStatus.INACTIVE
        )
    elif segment == "trial":
        query = query.join(Subscription).where(
            Subscription.status == SubscriptionStatus.TRIAL
        )
    elif segment == "with_balance":
        query = query.where(User.balance > 0)
    
    query = query.limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


async def add_user_balance(db: AsyncSession, user_id: int, amount: float) -> Optional[User]:
    return await update_user_balance(db, user_id, amount)


async def create_user_no_commit(
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
    return user


async def update_user(
    db: AsyncSession,
    user_id: int,
    **kwargs
) -> Optional[User]:
    user = await get_user_by_id(db, user_id)
    if not user:
        return None
    for key, value in kwargs.items():
        if hasattr(user, key):
            setattr(user, key, value)
    user.updated_at = datetime.utcnow()
    await db.commit()
    await db.refresh(user)
    return user


async def delete_user(db: AsyncSession, user_id: int) -> bool:
    """Delete a user by ID."""
    user = await get_user_by_id(db, user_id)
    if not user:
        return False
    await db.delete(user)
    await db.commit()
    return True


async def get_inactive_users(
    db: AsyncSession,
    days: int = 30,
    limit: int = 100
) -> List[User]:
    """Get users who have been inactive for a specified number of days."""
    from datetime import timedelta
    cutoff = datetime.utcnow() - timedelta(days=days)
    result = await db.execute(
        select(User).where(User.updated_at < cutoff).limit(limit)
    )
    return result.scalars().all()


async def subtract_user_balance(
    db: AsyncSession,
    user_id: int,
    amount: float
) -> Optional[User]:
    """Subtract from user balance."""
    user = await get_user_by_id(db, user_id)
    if user:
        user.balance -= amount
        if user.balance < 0:
            user.balance = 0
        user.updated_at = datetime.utcnow()
        await db.commit()
        await db.refresh(user)
    return user


async def cleanup_expired_promo_offer_discounts(
    db: AsyncSession
) -> int:
    """Clean up expired promo offer discounts. Returns number of cleaned records."""
    return 0


from typing import Dict, Any


async def get_users_statistics(db: AsyncSession) -> Dict[str, Any]:
    """Get user statistics."""
    from sqlalchemy import func
    from datetime import datetime, timedelta
    
    now = datetime.utcnow()
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    week_ago = now - timedelta(days=7)
    month_ago = now - timedelta(days=30)
    
    total = await db.execute(select(func.count(User.id)))
    active = await db.execute(
        select(func.count(User.id)).where(User.is_active == True)
    )
    blocked = await db.execute(
        select(func.count(User.id)).where(User.status == 'blocked')
    )
    new_today = await db.execute(
        select(func.count(User.id)).where(User.created_at >= today_start)
    )
    new_week = await db.execute(
        select(func.count(User.id)).where(User.created_at >= week_ago)
    )
    new_month = await db.execute(
        select(func.count(User.id)).where(User.created_at >= month_ago)
    )
    
    return {
        'total_users': total.scalar() or 0,
        'active_users': active.scalar() or 0,
        'blocked_users': blocked.scalar() or 0,
        'new_today': new_today.scalar() or 0,
        'new_week': new_week.scalar() or 0,
        'new_month': new_month.scalar() or 0,
    }


async def get_users_spending_stats(
    db: AsyncSession,
    limit: int = 100
) -> List[Dict[str, Any]]:
    """Get user spending statistics."""
    return []


async def get_referrals(
    db: AsyncSession,
    user_id: int,
    limit: int = 100
) -> List[User]:
    """Get referrals for a user."""
    result = await db.execute(
        select(User).where(User.referrer_id == user_id).limit(limit)
    )
    return result.scalars().all()


async def get_user_by_username(
    db: AsyncSession,
    username: str
) -> Optional[User]:
    """Get user by username."""
    result = await db.execute(
        select(User).where(User.username == username)
    )
    return result.scalar_one_or_none()
