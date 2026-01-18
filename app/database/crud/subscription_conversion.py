from datetime import datetime
from typing import Optional, List, Dict, Any
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models import SubscriptionConversion


async def create_conversion(
    db: AsyncSession,
    user_id: int,
    subscription_id: Optional[int] = None,
    from_status: Optional[str] = None,
    to_status: Optional[str] = None,
    amount_kopeks: int = 0
) -> SubscriptionConversion:
    conversion = SubscriptionConversion(
        user_id=user_id,
        subscription_id=subscription_id,
        from_status=from_status,
        to_status=to_status,
        amount_kopeks=amount_kopeks
    )
    db.add(conversion)
    await db.commit()
    await db.refresh(conversion)
    return conversion


async def get_conversion_by_id(
    db: AsyncSession,
    conversion_id: int
) -> Optional[SubscriptionConversion]:
    result = await db.execute(
        select(SubscriptionConversion).where(SubscriptionConversion.id == conversion_id)
    )
    return result.scalar_one_or_none()


async def get_conversions_by_user(
    db: AsyncSession,
    user_id: int,
    limit: int = 50
) -> List[SubscriptionConversion]:
    result = await db.execute(
        select(SubscriptionConversion)
        .where(SubscriptionConversion.user_id == user_id)
        .order_by(SubscriptionConversion.converted_at.desc())
        .limit(limit)
    )
    return result.scalars().all()


async def get_conversions_stats(db: AsyncSession) -> Dict[str, Any]:
    total_result = await db.execute(
        select(func.count(SubscriptionConversion.id))
    )
    total = total_result.scalar() or 0
    
    total_amount_result = await db.execute(
        select(func.sum(SubscriptionConversion.amount_kopeks))
    )
    total_amount = total_amount_result.scalar() or 0
    
    return {
        'total_conversions': total,
        'total_amount_kopeks': total_amount
    }


async def get_conversions_by_period(
    db: AsyncSession,
    start_date: datetime,
    end_date: datetime
) -> List[SubscriptionConversion]:
    result = await db.execute(
        select(SubscriptionConversion)
        .where(SubscriptionConversion.converted_at >= start_date)
        .where(SubscriptionConversion.converted_at <= end_date)
        .order_by(SubscriptionConversion.converted_at.desc())
    )
    return result.scalars().all()


async def create_subscription_conversion(
    db: AsyncSession,
    user_id: int,
    subscription_id: Optional[int] = None,
    from_status: Optional[str] = None,
    to_status: Optional[str] = None,
    amount_kopeks: int = 0,
    **kwargs
) -> SubscriptionConversion:
    """Alias for create_conversion for backward compatibility."""
    return await create_conversion(
        db=db,
        user_id=user_id,
        subscription_id=subscription_id,
        from_status=from_status,
        to_status=to_status,
        amount_kopeks=amount_kopeks
    )
