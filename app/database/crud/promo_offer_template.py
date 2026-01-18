from datetime import datetime
from typing import Optional, List, Dict, Any
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession


async def list_promo_offer_templates(
    db: AsyncSession,
    active_only: bool = False
) -> List[Dict[str, Any]]:
    return []


async def get_promo_offer_template_by_id(
    db: AsyncSession,
    template_id: int
) -> Optional[Dict[str, Any]]:
    return None


async def create_promo_offer_template(
    db: AsyncSession,
    name: str,
    **kwargs
) -> Dict[str, Any]:
    return {'id': 1, 'name': name}


async def update_promo_offer_template(
    db: AsyncSession,
    template_id: int,
    **kwargs
) -> Optional[Dict[str, Any]]:
    return None


async def delete_promo_offer_template(
    db: AsyncSession,
    template_id: int
) -> bool:
    return True


async def ensure_default_templates(db: AsyncSession) -> None:
    pass


async def get_active_promo_templates(db: AsyncSession) -> List[Dict[str, Any]]:
    return []
