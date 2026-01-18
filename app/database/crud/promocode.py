from datetime import datetime
from typing import Optional, List, Dict, Any
from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.database.models import PromoCode, PromoCodeUse


async def get_promocodes_list(
    db: AsyncSession,
    offset: int = 0,
    limit: int = 10,
    is_active: Optional[bool] = None
) -> List[PromoCode]:
    query = select(PromoCode).options(selectinload(PromoCode.promo_group))
    if is_active is not None:
        query = query.where(PromoCode.is_active == is_active)
    query = query.order_by(PromoCode.created_at.desc()).offset(offset).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


async def get_promocodes_count(
    db: AsyncSession,
    is_active: Optional[bool] = None
) -> int:
    query = select(func.count(PromoCode.id))
    if is_active is not None:
        query = query.where(PromoCode.is_active == is_active)
    result = await db.execute(query)
    return result.scalar() or 0


async def get_promocode_by_id(db: AsyncSession, promocode_id: int) -> Optional[PromoCode]:
    result = await db.execute(
        select(PromoCode)
        .options(selectinload(PromoCode.promo_group))
        .where(PromoCode.id == promocode_id)
    )
    return result.scalar_one_or_none()


async def get_promocode_by_code(db: AsyncSession, code: str) -> Optional[PromoCode]:
    result = await db.execute(
        select(PromoCode)
        .options(selectinload(PromoCode.promo_group))
        .where(func.lower(PromoCode.code) == code.lower())
    )
    return result.scalar_one_or_none()


async def create_promocode(
    db: AsyncSession,
    code: str,
    type: str = "balance",
    bonus_amount: float = 0.0,
    bonus_days: int = 0,
    balance_bonus_kopeks: int = 0,
    subscription_days: int = 0,
    promo_group_id: Optional[int] = None,
    max_uses: int = 1,
    first_purchase_only: bool = False,
    is_active: bool = True,
    valid_until: Optional[datetime] = None,
    created_by: Optional[int] = None
) -> PromoCode:
    promocode = PromoCode(
        code=code,
        type=type,
        bonus_amount=bonus_amount,
        bonus_days=bonus_days,
        balance_bonus_kopeks=balance_bonus_kopeks,
        subscription_days=subscription_days,
        promo_group_id=promo_group_id,
        max_uses=max_uses,
        first_purchase_only=first_purchase_only,
        is_active=is_active,
        valid_until=valid_until,
        created_by=created_by
    )
    db.add(promocode)
    await db.commit()
    await db.refresh(promocode)
    return promocode


async def update_promocode(
    db: AsyncSession,
    promocode_id: int,
    **kwargs
) -> Optional[PromoCode]:
    promocode = await get_promocode_by_id(db, promocode_id)
    if not promocode:
        return None
    
    for key, value in kwargs.items():
        if hasattr(promocode, key):
            setattr(promocode, key, value)
    
    promocode.updated_at = datetime.utcnow()
    await db.commit()
    await db.refresh(promocode)
    return promocode


async def delete_promocode(db: AsyncSession, promocode_id: int) -> bool:
    promocode = await get_promocode_by_id(db, promocode_id)
    if not promocode:
        return False
    await db.delete(promocode)
    await db.commit()
    return True


async def get_promocode_statistics(db: AsyncSession) -> Dict[str, Any]:
    total_result = await db.execute(select(func.count(PromoCode.id)))
    total = total_result.scalar() or 0
    
    active_result = await db.execute(
        select(func.count(PromoCode.id)).where(PromoCode.is_active == True)
    )
    active = active_result.scalar() or 0
    
    uses_result = await db.execute(select(func.count(PromoCodeUse.id)))
    total_uses = uses_result.scalar() or 0
    
    return {
        'total_codes': total,
        'active_codes': active,
        'inactive_codes': total - active,
        'total_uses': total_uses
    }


async def record_promocode_use(
    db: AsyncSession,
    user_id: int,
    promocode_id: int
) -> PromoCodeUse:
    use = PromoCodeUse(
        user_id=user_id,
        promo_code_id=promocode_id
    )
    db.add(use)
    
    promocode = await get_promocode_by_id(db, promocode_id)
    if promocode:
        promocode.current_uses += 1
        if promocode.current_uses >= promocode.max_uses:
            promocode.is_active = False
    
    await db.commit()
    await db.refresh(use)
    return use


async def has_user_used_promocode(
    db: AsyncSession,
    user_id: int,
    promocode_id: int
) -> bool:
    result = await db.execute(
        select(PromoCodeUse).where(
            and_(
                PromoCodeUse.user_id == user_id,
                PromoCodeUse.promo_code_id == promocode_id
            )
        )
    )
    return result.scalar_one_or_none() is not None


async def get_promocode_uses(
    db: AsyncSession,
    promocode_id: int,
    limit: int = 50
) -> List[PromoCodeUse]:
    result = await db.execute(
        select(PromoCodeUse)
        .where(PromoCodeUse.promo_code_id == promocode_id)
        .order_by(PromoCodeUse.used_at.desc())
        .limit(limit)
    )
    return result.scalars().all()
