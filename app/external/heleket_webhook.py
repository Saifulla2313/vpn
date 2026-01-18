import logging
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)


class HeleketWebhookHandler:
    """Stub handler for Heleket payment webhooks."""
    
    def __init__(self, secret_key: str = ""):
        self.secret_key = secret_key
    
    async def verify_signature(self, payload: str, signature: str) -> bool:
        """Verify webhook signature."""
        return False
    
    async def process_webhook(self, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Process incoming webhook."""
        logger.warning("HeleketWebhookHandler.process_webhook called but not implemented")
        return None
