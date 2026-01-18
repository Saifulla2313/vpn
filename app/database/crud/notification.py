from datetime import datetime
from typing import Optional, List, Dict, Any
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models import SentNotification


async def get_notifications_by_user(
    db: AsyncSession,
    user_id: int,
    limit: int = 50
) -> List[SentNotification]:
    result = await db.execute(
        select(SentNotification)
        .where(SentNotification.user_id == user_id)
        .order_by(SentNotification.sent_at.desc())
        .limit(limit)
    )
    return result.scalars().all()


async def create_notification(
    db: AsyncSession,
    user_id: int,
    notification_type: Optional[str] = None,
    message_id: Optional[int] = None
) -> SentNotification:
    notification = SentNotification(
        user_id=user_id,
        notification_type=notification_type,
        message_id=message_id
    )
    db.add(notification)
    await db.commit()
    await db.refresh(notification)
    return notification


async def get_notification_by_id(
    db: AsyncSession,
    notification_id: int
) -> Optional[SentNotification]:
    result = await db.execute(
        select(SentNotification).where(SentNotification.id == notification_id)
    )
    return result.scalar_one_or_none()


async def delete_notification(db: AsyncSession, notification_id: int) -> bool:
    notification = await get_notification_by_id(db, notification_id)
    if not notification:
        return False
    await db.delete(notification)
    await db.commit()
    return True


async def get_notifications_count(
    db: AsyncSession,
    user_id: Optional[int] = None,
    notification_type: Optional[str] = None
) -> int:
    query = select(func.count(SentNotification.id))
    if user_id:
        query = query.where(SentNotification.user_id == user_id)
    if notification_type:
        query = query.where(SentNotification.notification_type == notification_type)
    result = await db.execute(query)
    return result.scalar() or 0


async def get_notifications_stats(db: AsyncSession) -> Dict[str, Any]:
    total_result = await db.execute(
        select(func.count(SentNotification.id))
    )
    total = total_result.scalar() or 0
    
    by_type_result = await db.execute(
        select(
            SentNotification.notification_type,
            func.count(SentNotification.id)
        )
        .group_by(SentNotification.notification_type)
    )
    by_type = {row[0] or 'unknown': row[1] for row in by_type_result}
    
    return {
        'total_notifications': total,
        'by_type': by_type
    }


async def mark_notification_sent(
    db: AsyncSession,
    user_id: int,
    notification_type: str,
    message_id: Optional[int] = None
) -> SentNotification:
    return await create_notification(
        db,
        user_id=user_id,
        notification_type=notification_type,
        message_id=message_id
    )


async def has_received_notification(
    db: AsyncSession,
    user_id: int,
    notification_type: str,
    since: Optional[datetime] = None
) -> bool:
    query = select(SentNotification).where(
        SentNotification.user_id == user_id,
        SentNotification.notification_type == notification_type
    )
    if since:
        query = query.where(SentNotification.sent_at >= since)
    query = query.limit(1)
    
    result = await db.execute(query)
    return result.scalar_one_or_none() is not None


async def clear_notification_by_type(
    db: AsyncSession,
    user_id: int,
    notification_type: str
) -> bool:
    """Clear all notifications of a specific type for a user."""
    result = await db.execute(
        select(SentNotification).where(
            SentNotification.user_id == user_id,
            SentNotification.notification_type == notification_type
        )
    )
    notifications = result.scalars().all()
    for notification in notifications:
        await db.delete(notification)
    await db.commit()
    return True


async def notification_sent(
    db: AsyncSession,
    user_id: int,
    notification_type: str,
    since: Optional[datetime] = None
) -> bool:
    """Check if a notification has been sent to a user."""
    return await has_received_notification(db, user_id, notification_type, since)


async def record_notification(
    db: AsyncSession,
    user_id: int,
    notification_type: str,
    message_id: Optional[int] = None,
    **kwargs
) -> SentNotification:
    """Record a notification as sent."""
    return await create_notification(
        db,
        user_id=user_id,
        notification_type=notification_type,
        message_id=message_id
    )
