import logging
from typing import Any, Dict

from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)


class ReferralContestService:
    async def get_detailed_contest_stats(
        self,
        db: AsyncSession,
        contest_id: int,
    ) -> Dict[str, Any]:
        return {
            "total_participants": 0,
            "total_invited": 0,
            "paid_count": 0,
            "unpaid_count": 0,
            "subscription_total": 0,
            "deposit_total": 0,
            "total_paid_amount": 0,
            "participants": [],
        }

    async def sync_contest(
        self,
        db: AsyncSession,
        contest_id: int,
    ) -> Dict[str, Any]:
        return {
            "total_events": 0,
            "filtered_out_events": 0,
            "total_all_events": 0,
            "updated": 0,
            "skipped": 0,
            "paid_count": 0,
            "unpaid_count": 0,
            "subscription_total": 0,
            "deposit_total": 0,
        }


referral_contest_service = ReferralContestService()
