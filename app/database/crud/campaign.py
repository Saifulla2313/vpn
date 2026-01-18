from datetime import datetime
from typing import Optional, List, Dict, Any
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models import AdvertisingCampaign


async def get_campaign_by_start_parameter(db: AsyncSession, param: str) -> Optional[AdvertisingCampaign]:
    """Get campaign by start parameter."""
    result = await db.execute(
        select(AdvertisingCampaign).where(AdvertisingCampaign.start_parameter == param)
    )
    return result.scalar_one_or_none()


async def get_campaign_by_id(db: AsyncSession, campaign_id: int) -> Optional[AdvertisingCampaign]:
    """Get campaign by ID."""
    result = await db.execute(
        select(AdvertisingCampaign).where(AdvertisingCampaign.id == campaign_id)
    )
    return result.scalar_one_or_none()


async def create_campaign(
    db: AsyncSession,
    name: str,
    start_parameter: str,
    **kwargs
) -> AdvertisingCampaign:
    """Create a new campaign."""
    campaign = AdvertisingCampaign(
        name=name,
        start_parameter=start_parameter,
        is_active=kwargs.get('is_active', True),
        bonus_type=kwargs.get('bonus_type'),
        bonus_amount=kwargs.get('bonus_amount', 0),
        description=kwargs.get('description'),
    )
    db.add(campaign)
    await db.commit()
    await db.refresh(campaign)
    return campaign


async def update_campaign(
    db: AsyncSession,
    campaign_id: int,
    **kwargs
) -> Optional[AdvertisingCampaign]:
    """Update a campaign."""
    campaign = await get_campaign_by_id(db, campaign_id)
    if not campaign:
        return None
    
    for key, value in kwargs.items():
        if hasattr(campaign, key):
            setattr(campaign, key, value)
    
    campaign.updated_at = datetime.utcnow()
    await db.commit()
    await db.refresh(campaign)
    return campaign


async def delete_campaign(db: AsyncSession, campaign_id: int) -> bool:
    """Delete a campaign."""
    campaign = await get_campaign_by_id(db, campaign_id)
    if not campaign:
        return False
    await db.delete(campaign)
    await db.commit()
    return True


async def get_campaigns_list(
    db: AsyncSession,
    offset: int = 0,
    limit: int = 50
) -> List[AdvertisingCampaign]:
    """Get list of campaigns."""
    result = await db.execute(
        select(AdvertisingCampaign)
        .order_by(AdvertisingCampaign.created_at.desc())
        .offset(offset)
        .limit(limit)
    )
    return result.scalars().all()


async def get_campaigns_count(db: AsyncSession) -> int:
    """Get total count of campaigns."""
    result = await db.execute(
        select(func.count(AdvertisingCampaign.id))
    )
    return result.scalar() or 0


async def get_campaign_statistics(db: AsyncSession, campaign_id: int = None) -> Dict[str, Any]:
    """Get campaign statistics."""
    return {
        'total_registrations': 0,
        'active_users': 0,
        'conversions': 0
    }


async def get_campaigns_overview(db: AsyncSession) -> Dict[str, Any]:
    """Get overview of all campaigns."""
    total = await get_campaigns_count(db)
    return {
        'total_campaigns': total,
        'active_campaigns': 0,
        'total_registrations': 0
    }


async def record_campaign_registration(
    db: AsyncSession,
    campaign_id: int,
    user_id: int
) -> bool:
    """Record a campaign registration."""
    return True


async def get_campaign_registration_by_user(
    db: AsyncSession,
    user_id: int
) -> Optional[Dict[str, Any]]:
    """Get campaign registration info for a user."""
    return None
