import logging
from typing import Any, Dict, Optional, Tuple

from aiogram import Bot

logger = logging.getLogger(__name__)


class TrafficMonitoringService:
    async def check_user_traffic_threshold(
        self,
        user_id: int,
        subscription_id: Optional[int] = None,
    ) -> Tuple[bool, Dict[str, Any]]:
        is_exceeded = False
        traffic_info = {
            "used_bytes": 0,
            "limit_bytes": 0,
            "percentage": 0.0,
        }
        return is_exceeded, traffic_info

    async def process_suspicious_traffic(
        self,
        user_id: int,
        traffic_info: Dict[str, Any],
        bot: Optional[Bot] = None,
    ) -> None:
        logger.warning(
            "Suspicious traffic detected for user %s: %s",
            user_id,
            traffic_info,
        )

    async def get_user_traffic_stats(
        self,
        user_id: int,
    ) -> Dict[str, Any]:
        return {
            "total_used": 0,
            "limit": 0,
            "percentage": 0.0,
        }


class TrafficMonitoringScheduler:
    def __init__(self) -> None:
        self._bot: Optional[Bot] = None

    def set_bot(self, bot: Bot) -> None:
        self._bot = bot

    async def start(self) -> None:
        pass

    async def stop(self) -> None:
        pass


traffic_monitoring_service = TrafficMonitoringService()
traffic_monitoring_scheduler = TrafficMonitoringScheduler()
