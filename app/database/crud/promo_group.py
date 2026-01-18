from datetime import datetime
from typing import Optional, List, Dict, Any
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.database.models import PromoGroup, User


async def get_promo_groups_with_counts(
    db: AsyncSession,
    include_inactive: bool = True
) -> List[Dict[str, Any]]:
    query = select(PromoGroup)
    if not include_inactive:
        query = query.where(PromoGroup.is_active == True)
    query = query.order_by(PromoGroup.priority.desc(), PromoGroup.id)
    result = await db.execute(query)
    groups = result.scalars().all()
    
    results = []
    for group in groups:
        member_count = await count_promo_group_members(db, group.id)
        results.append({
            'group': group,
            'member_count': member_count
        })
    return results


async def get_promo_group_by_id(db: AsyncSession, group_id: int) -> Optional[PromoGroup]:
    result = await db.execute(
        select(PromoGroup).where(PromoGroup.id == group_id)
    )
    return result.scalar_one_or_none()


async def create_promo_group(
    db: AsyncSession,
    name: str,
    priority: int = 0,
    server_discount_percent: int = 0,
    traffic_discount_percent: int = 0,
    device_discount_percent: int = 0,
    period_discounts: Optional[Dict] = None,
    auto_assign_total_spent_kopeks: Optional[int] = None,
    apply_discounts_to_addons: bool = True,
    is_default: bool = False,
    is_active: bool = True
) -> PromoGroup:
    group = PromoGroup(
        name=name,
        priority=priority,
        server_discount_percent=server_discount_percent,
        traffic_discount_percent=traffic_discount_percent,
        device_discount_percent=device_discount_percent,
        period_discounts=period_discounts or {},
        auto_assign_total_spent_kopeks=auto_assign_total_spent_kopeks,
        apply_discounts_to_addons=apply_discounts_to_addons,
        is_default=is_default,
        is_active=is_active
    )
    db.add(group)
    await db.commit()
    await db.refresh(group)
    return group


async def update_promo_group(
    db: AsyncSession,
    group_id: int,
    **kwargs
) -> Optional[PromoGroup]:
    group = await get_promo_group_by_id(db, group_id)
    if not group:
        return None
    
    for key, value in kwargs.items():
        if hasattr(group, key):
            setattr(group, key, value)
    
    group.updated_at = datetime.utcnow()
    await db.commit()
    await db.refresh(group)
    return group


async def delete_promo_group(db: AsyncSession, group_id: int) -> bool:
    group = await get_promo_group_by_id(db, group_id)
    if not group:
        return False
    await db.delete(group)
    await db.commit()
    return True


async def get_promo_group_members(
    db: AsyncSession,
    group_id: int,
    limit: int = 100,
    offset: int = 0
) -> List[User]:
    return []


async def count_promo_group_members(db: AsyncSession, group_id: int) -> int:
    return 0


async def get_default_promo_group(db: AsyncSession) -> Optional[PromoGroup]:
    result = await db.execute(
        select(PromoGroup)
        .where(PromoGroup.is_default == True)
        .where(PromoGroup.is_active == True)
        .limit(1)
    )
    return result.scalar_one_or_none()


async def set_default_promo_group(db: AsyncSession, group_id: int) -> Optional[PromoGroup]:
    await db.execute(
        select(PromoGroup).where(PromoGroup.is_default == True)
    )
    result = await db.execute(
        select(PromoGroup).where(PromoGroup.is_default == True)
    )
    for group in result.scalars().all():
        group.is_default = False
    
    group = await get_promo_group_by_id(db, group_id)
    if group:
        group.is_default = True
        await db.commit()
        await db.refresh(group)
    
    return group
