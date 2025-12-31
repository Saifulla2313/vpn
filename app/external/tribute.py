import hashlib
import hmac
import logging
from app.config import settings

logger = logging.getLogger(__name__)


class TributeService:
    def __init__(self):
        self.api_key = settings.TRIBUTE_API_KEY
    
    def verify_webhook_signature(self, payload: str, signature: str) -> bool:
        if not self.api_key:
            return False
        
        expected = hmac.new(
            self.api_key.encode(),
            payload.encode(),
            hashlib.sha256
        ).hexdigest()
        
        return hmac.compare_digest(expected, signature)
