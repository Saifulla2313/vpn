import logging
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)


class Pal24APIError(Exception):
    """Exception for Pal24 API errors."""
    pass


class Pal24Client:
    """Stub client for Pal24 payment integration."""
    
    def __init__(self, api_key: str = "", merchant_id: str = ""):
        self.api_key = api_key
        self.merchant_id = merchant_id
        self._configured = bool(api_key and merchant_id)
    
    @property
    def is_configured(self) -> bool:
        return self._configured
    
    async def create_payment(
        self,
        amount: float,
        currency: str = "RUB",
        order_id: Optional[str] = None,
        description: Optional[str] = None,
        **kwargs
    ) -> Optional[Dict[str, Any]]:
        """Create a payment request."""
        logger.warning("Pal24Client.create_payment called but not implemented")
        return None
    
    async def check_payment_status(self, payment_id: str) -> Optional[Dict[str, Any]]:
        """Check payment status."""
        logger.warning("Pal24Client.check_payment_status called but not implemented")
        return None
    
    async def verify_callback(self, data: Dict[str, Any]) -> bool:
        """Verify callback signature."""
        return False
