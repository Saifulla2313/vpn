from datetime import datetime
from typing import Optional, List, Dict, Any
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models import SubscriptionEvent


async def create_subscription_event(
    db: AsyncSession,
    event_type: str,
    user_id: int,
    subscription_id: Optional[int] = None,
    transaction_id: Optional[int] = None,
    amount_kopeks: Optional[int] = None,
    currency: Optional[str] = None,
    message: Optional[str] = None,
    extra: Optional[Dict] = None
) -> SubscriptionEvent:
    event = SubscriptionEvent(
        event_type=event_type,
        user_id=user_id,
        subscription_id=subscription_id,
        transaction_id=transaction_id,
        amount_kopeks=amount_kopeks,
        currency=currency,
        message=message,
        extra=extra or {}
    )
    db.add(event)
    await db.commit()
    await db.refresh(event)
    return event


async def get_subscription_event_by_id(
    db: AsyncSession,
    event_id: int
) -> Optional[SubscriptionEvent]:
    result = await db.execute(
        select(SubscriptionEvent).where(SubscriptionEvent.id == event_id)
    )
    return result.scalar_one_or_none()


async def get_events_by_user(
    db: AsyncSession,
    user_id: int,
    limit: int = 50
) -> List[SubscriptionEvent]:
    result = await db.execute(
        select(SubscriptionEvent)
        .where(SubscriptionEvent.user_id == user_id)
        .order_by(SubscriptionEvent.occurred_at.desc())
        .limit(limit)
    )
    return result.scalars().all()


async def get_events_by_subscription(
    db: AsyncSession,
    subscription_id: int,
    limit: int = 50
) -> List[SubscriptionEvent]:
    result = await db.execute(
        select(SubscriptionEvent)
        .where(SubscriptionEvent.subscription_id == subscription_id)
        .order_by(SubscriptionEvent.occurred_at.desc())
        .limit(limit)
    )
    return result.scalars().all()


async def get_events_by_type(
    db: AsyncSession,
    event_type: str,
    limit: int = 100
) -> List[SubscriptionEvent]:
    result = await db.execute(
        select(SubscriptionEvent)
        .where(SubscriptionEvent.event_type == event_type)
        .order_by(SubscriptionEvent.occurred_at.desc())
        .limit(limit)
    )
    return result.scalars().all()


async def get_events_stats(db: AsyncSession) -> Dict[str, Any]:
    total_result = await db.execute(
        select(func.count(SubscriptionEvent.id))
    )
    total = total_result.scalar() or 0
    
    by_type_result = await db.execute(
        select(
            SubscriptionEvent.event_type,
            func.count(SubscriptionEvent.id)
        )
        .group_by(SubscriptionEvent.event_type)
    )
    by_type = {row[0]: row[1] for row in by_type_result}
    
    return {
        'total_events': total,
        'by_type': by_type
    }


async def get_recent_events(
    db: AsyncSession,
    limit: int = 100
) -> List[SubscriptionEvent]:
    result = await db.execute(
        select(SubscriptionEvent)
        .order_by(SubscriptionEvent.occurred_at.desc())
        .limit(limit)
    )
    return result.scalars().all()
