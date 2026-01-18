import logging
from typing import Any, Dict

logger = logging.getLogger(__name__)


class NalogoQueueService:
    async def get_status(self) -> Dict[str, Any]:
        return {
            "queue_length": 0,
            "total_amount": 0.0,
            "running": False,
            "pending_verification_count": 0,
            "pending_verification_amount": 0.0,
        }

    async def force_process(self) -> Dict[str, Any]:
        return {
            "message": "Queue is empty",
            "processed": 0,
            "remaining": 0,
        }

    async def add_to_queue(
        self,
        payment_id: str,
        amount: float,
        description: str,
    ) -> bool:
        return True


nalogo_queue_service = NalogoQueueService()
