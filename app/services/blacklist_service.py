import logging
from typing import List, Optional, Tuple

logger = logging.getLogger(__name__)


class BlacklistService:
    def is_blacklist_check_enabled(self) -> bool:
        return False

    def get_blacklist_github_url(self) -> Optional[str]:
        return None

    async def get_all_blacklisted_users(self) -> List[Tuple[int, Optional[str], str]]:
        return []

    async def force_update_blacklist(self) -> Tuple[bool, str]:
        return True, "Blacklist updated successfully"

    async def check_user(self, telegram_id: int) -> bool:
        return False


blacklist_service = BlacklistService()
