import logging
from datetime import datetime
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)


class ContestRotationService:
    def _build_payload_for_template(self, template: Any) -> Dict[str, Any]:
        return {
            "template_id": getattr(template, "id", None),
            "name": getattr(template, "name", ""),
            "prize_type": getattr(template, "prize_type", "days"),
            "prize_value": getattr(template, "prize_value", "1"),
        }

    async def _announce_round_start(
        self,
        template: Any,
        starts_at: datetime,
        ends_at: Optional[datetime] = None,
    ) -> None:
        logger.info(
            "Round started for template %s at %s",
            getattr(template, "name", "unknown"),
            starts_at,
        )

    async def close_all_active_rounds(self) -> int:
        return 0

    async def reset_all_attempts(self) -> int:
        return 0

    async def start_all_contests(self) -> int:
        return 0


contest_rotation_service = ContestRotationService()
