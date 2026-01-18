from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models import ReferralEarning, User


async def get_referral_statistics(db: AsyncSession) -> Dict[str, Any]:
    users_with_refs = await db.execute(
        select(func.count(func.distinct(User.referrer_id)))
        .where(User.referrer_id.isnot(None))
    )
    users_with_referrals = users_with_refs.scalar() or 0
    
    active_referrers = await db.execute(
        select(func.count(func.distinct(ReferralEarning.referrer_id)))
    )
    active_refs = active_referrers.scalar() or 0
    
    total_paid = await db.execute(
        select(func.sum(ReferralEarning.amount_kopeks))
    )
    total_paid_kopeks = total_paid.scalar() or 0
    
    now = datetime.utcnow()
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    week_start = today_start - timedelta(days=7)
    month_start = today_start - timedelta(days=30)
    
    today_result = await db.execute(
        select(func.sum(ReferralEarning.amount_kopeks))
        .where(ReferralEarning.created_at >= today_start)
    )
    today_earnings = today_result.scalar() or 0
    
    week_result = await db.execute(
        select(func.sum(ReferralEarning.amount_kopeks))
        .where(ReferralEarning.created_at >= week_start)
    )
    week_earnings = week_result.scalar() or 0
    
    month_result = await db.execute(
        select(func.sum(ReferralEarning.amount_kopeks))
        .where(ReferralEarning.created_at >= month_start)
    )
    month_earnings = month_result.scalar() or 0
    
    top_referrers_query = await db.execute(
        select(
            ReferralEarning.referrer_id,
            func.sum(ReferralEarning.amount_kopeks).label('total_earned'),
            func.count(func.distinct(ReferralEarning.user_id)).label('referrals_count')
        )
        .group_by(ReferralEarning.referrer_id)
        .order_by(func.sum(ReferralEarning.amount_kopeks).desc())
        .limit(10)
    )
    top_referrers = []
    for row in top_referrers_query:
        top_referrers.append({
            'user_id': row[0],
            'total_earned_kopeks': row[1] or 0,
            'referrals_count': row[2] or 0
        })
    
    return {
        'users_with_referrals': users_with_referrals,
        'active_referrers': active_refs,
        'total_paid_kopeks': total_paid_kopeks,
        'today_earnings_kopeks': today_earnings,
        'week_earnings_kopeks': week_earnings,
        'month_earnings_kopeks': month_earnings,
        'top_referrers': top_referrers
    }


async def get_top_referrers_by_period(
    db: AsyncSession,
    start_date: datetime,
    end_date: datetime,
    limit: int = 10
) -> List[Dict[str, Any]]:
    result = await db.execute(
        select(
            ReferralEarning.referrer_id,
            func.sum(ReferralEarning.amount_kopeks).label('total_earned'),
            func.count(func.distinct(ReferralEarning.user_id)).label('referrals_count')
        )
        .where(and_(
            ReferralEarning.created_at >= start_date,
            ReferralEarning.created_at <= end_date
        ))
        .group_by(ReferralEarning.referrer_id)
        .order_by(func.sum(ReferralEarning.amount_kopeks).desc())
        .limit(limit)
    )
    
    referrers = []
    for row in result:
        referrers.append({
            'user_id': row[0],
            'total_earned_kopeks': row[1] or 0,
            'referrals_count': row[2] or 0
        })
    return referrers


async def get_user_referral_stats(db: AsyncSession, user_id: int) -> Dict[str, Any]:
    referrals_count = await db.execute(
        select(func.count(User.id)).where(User.referrer_id == user_id)
    )
    total_referrals = referrals_count.scalar() or 0
    
    earnings_sum = await db.execute(
        select(func.sum(ReferralEarning.amount_kopeks))
        .where(ReferralEarning.referrer_id == user_id)
    )
    total_earnings = earnings_sum.scalar() or 0
    
    return {
        'user_id': user_id,
        'total_referrals': total_referrals,
        'total_earnings_kopeks': total_earnings
    }


async def get_referral_earnings_by_user(
    db: AsyncSession,
    user_id: int,
    limit: int = 50
) -> List[ReferralEarning]:
    result = await db.execute(
        select(ReferralEarning)
        .where(ReferralEarning.referrer_id == user_id)
        .order_by(ReferralEarning.created_at.desc())
        .limit(limit)
    )
    return result.scalars().all()


async def create_referral_earning(
    db: AsyncSession,
    user_id: int,
    referrer_id: int,
    amount_kopeks: int,
    source: Optional[str] = None,
    description: Optional[str] = None
) -> ReferralEarning:
    earning = ReferralEarning(
        user_id=user_id,
        referrer_id=referrer_id,
        amount_kopeks=amount_kopeks,
        source=source,
        description=description
    )
    db.add(earning)
    await db.commit()
    await db.refresh(earning)
    return earning
