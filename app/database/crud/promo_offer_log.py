from datetime import datetime
from typing import Optional, List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession


async def list_promo_offer_logs(
    db: AsyncSession,
    limit: int = 100,
    offset: int = 0,
    user_id: Optional[int] = None,
    template_id: Optional[int] = None
) -> List[Dict[str, Any]]:
    return []


async def get_promo_offer_log_by_id(
    db: AsyncSession,
    log_id: int
) -> Optional[Dict[str, Any]]:
    return None


async def create_promo_offer_log(
    db: AsyncSession,
    user_id: int,
    template_id: Optional[int] = None,
    offer_type: Optional[str] = None,
    status: Optional[str] = None,
    **kwargs
) -> Dict[str, Any]:
    return {
        'id': 1,
        'user_id': user_id,
        'template_id': template_id,
        'offer_type': offer_type,
        'status': status,
        'created_at': datetime.utcnow()
    }


async def get_promo_offer_logs_count(
    db: AsyncSession,
    user_id: Optional[int] = None
) -> int:
    return 0


async def get_promo_offer_logs_stats(db: AsyncSession) -> Dict[str, Any]:
    return {
        'total_logs': 0
    }


async def log_promo_offer_action(
    db: AsyncSession,
    user_id: int,
    action: str,
    offer_id: Optional[int] = None,
    template_id: Optional[int] = None,
    details: Optional[Dict[str, Any]] = None,
    **kwargs
) -> Dict[str, Any]:
    """Log a promo offer action."""
    return {
        'id': 1,
        'user_id': user_id,
        'action': action,
        'offer_id': offer_id,
        'template_id': template_id,
        'details': details or {},
        'created_at': datetime.utcnow()
    }
