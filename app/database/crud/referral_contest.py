from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models import ReferralEarning, User


async def list_referral_contests(
    db: AsyncSession,
    limit: int = 20,
    offset: int = 0
) -> List[Dict[str, Any]]:
    return []


async def get_referral_contests_count(db: AsyncSession) -> int:
    return 0


async def get_referral_contest(db: AsyncSession, contest_id: int) -> Optional[Dict[str, Any]]:
    return None


async def create_referral_contest(
    db: AsyncSession,
    name: str,
    start_at: datetime,
    end_at: datetime,
    prize_text: Optional[str] = None,
    is_active: bool = True,
    **kwargs
) -> Dict[str, Any]:
    return {
        'id': 1,
        'name': name,
        'start_at': start_at,
        'end_at': end_at,
        'prize_text': prize_text,
        'is_active': is_active
    }


async def update_referral_contest(
    db: AsyncSession,
    contest_id: int,
    **kwargs
) -> Optional[Dict[str, Any]]:
    return None


async def delete_referral_contest(db: AsyncSession, contest_id: int) -> bool:
    return True


async def toggle_referral_contest(db: AsyncSession, contest_id: int) -> Optional[Dict[str, Any]]:
    return None


async def get_contest_leaderboard(
    db: AsyncSession,
    contest_id: int,
    limit: int = 10
) -> List[Dict[str, Any]]:
    return []


async def get_contest_events_count(db: AsyncSession, contest_id: int) -> int:
    return 0


async def debug_contest_transactions(db: AsyncSession, contest_id: int) -> Dict[str, Any]:
    return {
        'contest_id': contest_id,
        'transactions': [],
        'total_amount': 0
    }
