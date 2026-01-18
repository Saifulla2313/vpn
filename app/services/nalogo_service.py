import logging
from datetime import date
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class NaloGoService:
    async def get_pending_verification_receipts(self) -> List[Dict[str, Any]]:
        return []

    async def mark_pending_as_verified(
        self,
        payment_id: str,
        receipt_uuid: Optional[str] = None,
        was_created: bool = True,
    ) -> bool:
        return True

    async def retry_pending_receipt(self, payment_id: str) -> Optional[str]:
        return None

    async def clear_pending_verification(self) -> int:
        return 0

    async def get_incomes(
        self,
        from_date: date,
        to_date: date,
        limit: int = 100,
    ) -> List[Dict[str, Any]]:
        return []

    async def create_receipt(
        self,
        payment_id: str,
        amount: float,
        description: str,
    ) -> Optional[str]:
        return None
