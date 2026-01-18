import logging
import re
from typing import List, Tuple, Optional

from aiogram import Bot
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)


class BulkBanService:
    async def parse_telegram_ids_from_text(self, input_text: str) -> List[int]:
        ids = []
        parts = re.split(r'[\s,;]+', input_text.strip())
        for part in parts:
            part = part.strip()
            if part.isdigit():
                ids.append(int(part))
        return ids

    async def ban_users_by_telegram_ids(
        self,
        db: AsyncSession,
        admin_user_id: int,
        telegram_ids: List[int],
        reason: str,
        bot: Optional[Bot] = None,
        notify_admin: bool = True,
        admin_name: Optional[str] = None,
    ) -> Tuple[int, int, List[int]]:
        successfully_banned = 0
        not_found = len(telegram_ids)
        error_ids: List[int] = []
        return successfully_banned, not_found, error_ids


bulk_ban_service = BulkBanService()
