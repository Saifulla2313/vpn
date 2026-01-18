import logging
from typing import Any, Dict, List, Optional, Tuple

from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)


class ReferralWithdrawalService:
    async def get_pending_requests(self, db: AsyncSession) -> List[Any]:
        return []

    def format_analysis_for_admin(self, analysis: Dict[str, Any]) -> str:
        if not analysis:
            return ""

        lines = ["📊 <b>Анализ рисков:</b>"]

        if "referral_count" in analysis:
            lines.append(f"• Рефералов: {analysis['referral_count']}")
        if "total_earned" in analysis:
            lines.append(f"• Всего заработано: {analysis['total_earned']} ₽")
        if "risk_factors" in analysis:
            for factor in analysis["risk_factors"]:
                lines.append(f"⚠️ {factor}")

        return "\n".join(lines)

    async def approve_request(
        self,
        db: AsyncSession,
        request_id: int,
        admin_id: int,
    ) -> Tuple[bool, Optional[str]]:
        return False, "Not implemented"

    async def reject_request(
        self,
        db: AsyncSession,
        request_id: int,
        admin_id: int,
        reason: str,
    ) -> bool:
        return False

    async def complete_request(
        self,
        db: AsyncSession,
        request_id: int,
        admin_id: int,
    ) -> bool:
        return False

    async def create_withdrawal_request(
        self,
        db: AsyncSession,
        user_id: int,
        amount_kopeks: int,
        payment_details: str,
    ) -> Tuple[bool, Optional[str], Optional[Any]]:
        return False, "Not implemented", None


referral_withdrawal_service = ReferralWithdrawalService()
