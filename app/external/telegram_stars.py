import logging
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)


class TelegramStarsService:
    """Stub service for Telegram Stars payment integration."""
    
    def __init__(self, bot=None):
        self._bot = bot
        self._configured = False
    
    @property
    def is_configured(self) -> bool:
        return self._configured
    
    def set_bot(self, bot):
        self._bot = bot
    
    async def create_invoice(
        self,
        user_id: int,
        amount: int,
        title: str = "",
        description: str = "",
        **kwargs
    ) -> Optional[str]:
        """Create a Telegram Stars invoice."""
        logger.warning("TelegramStarsService.create_invoice called but not implemented")
        return None
    
    async def check_payment(self, charge_id: str) -> Optional[Dict[str, Any]]:
        """Check payment status."""
        logger.warning("TelegramStarsService.check_payment called but not implemented")
        return None
    
    async def refund_payment(self, user_id: int, charge_id: str) -> bool:
        """Refund a Telegram Stars payment."""
        logger.warning("TelegramStarsService.refund_payment called but not implemented")
        return False
