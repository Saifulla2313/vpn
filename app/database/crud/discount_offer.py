from datetime import datetime
from typing import Optional, List, Dict, Any
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models import DiscountOffer


async def list_discount_offers(
    db: AsyncSession,
    active_only: bool = False,
    limit: int = 100,
    offset: int = 0
) -> List[DiscountOffer]:
    query = select(DiscountOffer)
    if active_only:
        query = query.where(DiscountOffer.is_active == True)
    query = query.order_by(DiscountOffer.created_at.desc()).offset(offset).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


async def get_discount_offer_by_id(
    db: AsyncSession,
    offer_id: int
) -> Optional[DiscountOffer]:
    result = await db.execute(
        select(DiscountOffer).where(DiscountOffer.id == offer_id)
    )
    return result.scalar_one_or_none()


async def create_discount_offer(
    db: AsyncSession,
    name: str,
    discount_percent: int = 0,
    discount_kopeks: int = 0,
    applies_to: Optional[str] = None,
    is_active: bool = True,
    valid_from: Optional[datetime] = None,
    valid_until: Optional[datetime] = None
) -> DiscountOffer:
    offer = DiscountOffer(
        name=name,
        discount_percent=discount_percent,
        discount_kopeks=discount_kopeks,
        applies_to=applies_to,
        is_active=is_active,
        valid_from=valid_from,
        valid_until=valid_until
    )
    db.add(offer)
    await db.commit()
    await db.refresh(offer)
    return offer


async def update_discount_offer(
    db: AsyncSession,
    offer_id: int,
    **kwargs
) -> Optional[DiscountOffer]:
    offer = await get_discount_offer_by_id(db, offer_id)
    if not offer:
        return None
    
    for key, value in kwargs.items():
        if hasattr(offer, key):
            setattr(offer, key, value)
    
    offer.updated_at = datetime.utcnow()
    await db.commit()
    await db.refresh(offer)
    return offer


async def delete_discount_offer(db: AsyncSession, offer_id: int) -> bool:
    offer = await get_discount_offer_by_id(db, offer_id)
    if not offer:
        return False
    await db.delete(offer)
    await db.commit()
    return True


async def upsert_discount_offer(
    db: AsyncSession,
    offer_id: Optional[int] = None,
    **kwargs
) -> DiscountOffer:
    if offer_id:
        existing = await get_discount_offer_by_id(db, offer_id)
        if existing:
            for key, value in kwargs.items():
                if hasattr(existing, key):
                    setattr(existing, key, value)
            existing.updated_at = datetime.utcnow()
            await db.commit()
            await db.refresh(existing)
            return existing
    
    name = kwargs.pop('name', 'New Discount')
    return await create_discount_offer(db, name=name, **kwargs)


async def get_active_discount_offers(db: AsyncSession) -> List[DiscountOffer]:
    now = datetime.utcnow()
    query = select(DiscountOffer).where(
        DiscountOffer.is_active == True
    )
    result = await db.execute(query)
    offers = result.scalars().all()
    
    active_offers = []
    for offer in offers:
        if offer.valid_from and offer.valid_from > now:
            continue
        if offer.valid_until and offer.valid_until < now:
            continue
        active_offers.append(offer)
    
    return active_offers


async def get_offer_by_id(db: AsyncSession, offer_id: int) -> Optional[DiscountOffer]:
    """Alias for get_discount_offer_by_id."""
    return await get_discount_offer_by_id(db, offer_id)


async def get_latest_claimed_offer_for_user(
    db: AsyncSession,
    user_id: int
) -> Optional[DiscountOffer]:
    """Get the latest claimed discount offer for a user."""
    result = await db.execute(
        select(DiscountOffer)
        .where(DiscountOffer.is_active == True)
        .order_by(DiscountOffer.created_at.desc())
        .limit(1)
    )
    return result.scalar_one_or_none()


async def list_active_discount_offers_for_user(
    db: AsyncSession,
    user_id: int
) -> List[DiscountOffer]:
    """List active discount offers available for a specific user."""
    return await get_active_discount_offers(db)


async def mark_offer_claimed(
    db: AsyncSession,
    offer_id: int,
    user_id: int
) -> Optional[DiscountOffer]:
    """Mark an offer as claimed by a user."""
    offer = await get_discount_offer_by_id(db, offer_id)
    if offer:
        offer.updated_at = datetime.utcnow()
        await db.commit()
        await db.refresh(offer)
    return offer


async def count_discount_offers(
    db: AsyncSession,
    active_only: bool = False
) -> int:
    """Count discount offers."""
    query = select(func.count(DiscountOffer.id))
    if active_only:
        query = query.where(DiscountOffer.is_active == True)
    result = await db.execute(query)
    return result.scalar() or 0


async def deactivate_expired_offers(db: AsyncSession) -> int:
    """Deactivate expired discount offers."""
    now = datetime.utcnow()
    result = await db.execute(
        select(DiscountOffer).where(
            DiscountOffer.is_active == True,
            DiscountOffer.valid_until < now
        )
    )
    expired_offers = result.scalars().all()
    
    count = 0
    for offer in expired_offers:
        offer.is_active = False
        offer.updated_at = now
        count += 1
    
    if count > 0:
        await db.commit()
    
    return count
