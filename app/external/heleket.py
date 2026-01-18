import logging
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)


class HeleketService:
    """Stub service for Heleket payment integration."""
    
    def __init__(self):
        self._configured = False
    
    @property
    def is_configured(self) -> bool:
        return self._configured
    
    async def create_payment(
        self,
        amount: float,
        currency: str = "RUB",
        description: Optional[str] = None,
        **kwargs
    ) -> Optional[Dict[str, Any]]:
        """Create a payment request."""
        logger.warning("HeleketService.create_payment called but not implemented")
        return None
    
    async def check_payment_status(self, payment_id: str) -> Optional[Dict[str, Any]]:
        """Check payment status."""
        logger.warning("HeleketService.check_payment_status called but not implemented")
        return None
    
    async def verify_webhook(self, payload: Dict[str, Any], signature: str) -> bool:
        """Verify webhook signature."""
        return False
