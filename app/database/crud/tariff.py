from datetime import datetime
from typing import Optional, List, Dict, Any
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models import Tariff, Subscription


async def get_all_tariffs(
    db: AsyncSession,
    include_inactive: bool = True
) -> List[Tariff]:
    query = select(Tariff)
    if not include_inactive:
        query = query.where(Tariff.is_active == True)
    query = query.order_by(Tariff.sort_order, Tariff.id)
    result = await db.execute(query)
    return result.scalars().all()


async def get_tariff_by_id(db: AsyncSession, tariff_id: int) -> Optional[Tariff]:
    result = await db.execute(select(Tariff).where(Tariff.id == tariff_id))
    return result.scalar_one_or_none()


async def create_tariff(
    db: AsyncSession,
    name: str,
    price_kopeks: int = 0,
    duration_days: int = 30,
    description: Optional[str] = None,
    traffic_gb: Optional[int] = None,
    device_limit: Optional[int] = None,
    is_active: bool = True,
    sort_order: int = 0
) -> Tariff:
    tariff = Tariff(
        name=name,
        price_kopeks=price_kopeks,
        duration_days=duration_days,
        description=description,
        traffic_gb=traffic_gb,
        device_limit=device_limit,
        is_active=is_active,
        sort_order=sort_order
    )
    db.add(tariff)
    await db.commit()
    await db.refresh(tariff)
    return tariff


async def update_tariff(
    db: AsyncSession,
    tariff_id: int,
    **kwargs
) -> Optional[Tariff]:
    tariff = await get_tariff_by_id(db, tariff_id)
    if not tariff:
        return None
    
    for key, value in kwargs.items():
        if hasattr(tariff, key):
            setattr(tariff, key, value)
    
    tariff.updated_at = datetime.utcnow()
    await db.commit()
    await db.refresh(tariff)
    return tariff


async def delete_tariff(db: AsyncSession, tariff_id: int) -> bool:
    tariff = await get_tariff_by_id(db, tariff_id)
    if not tariff:
        return False
    await db.delete(tariff)
    await db.commit()
    return True


async def get_tariff_subscriptions_count(db: AsyncSession, tariff_id: int) -> int:
    return 0


async def get_tariffs_with_subscriptions_count(db: AsyncSession) -> List[Dict[str, Any]]:
    tariffs = await get_all_tariffs(db)
    result = []
    for tariff in tariffs:
        count = await get_tariff_subscriptions_count(db, tariff.id)
        result.append({
            'tariff': tariff,
            'subscriptions_count': count
        })
    return result


async def set_trial_tariff(db: AsyncSession, tariff_id: int) -> Optional[Tariff]:
    tariff = await get_tariff_by_id(db, tariff_id)
    return tariff


async def clear_trial_tariff(db: AsyncSession) -> None:
    pass


async def add_promo_group_to_tariff(
    db: AsyncSession,
    tariff_id: int,
    promo_group_id: int
) -> Optional[Tariff]:
    tariff = await get_tariff_by_id(db, tariff_id)
    return tariff


async def remove_promo_group_from_tariff(
    db: AsyncSession,
    tariff_id: int,
    promo_group_id: int
) -> Optional[Tariff]:
    tariff = await get_tariff_by_id(db, tariff_id)
    return tariff


async def set_tariff_promo_groups(
    db: AsyncSession,
    tariff_id: int,
    promo_group_ids: List[int]
) -> Optional[Tariff]:
    tariff = await get_tariff_by_id(db, tariff_id)
    return tariff


async def get_tariffs_for_user(
    db: AsyncSession,
    user_id: int
) -> List[Tariff]:
    return await get_all_tariffs(db, include_inactive=False)
