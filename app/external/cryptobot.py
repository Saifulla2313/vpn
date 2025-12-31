import hashlib
import hmac
import logging
from app.config import settings

logger = logging.getLogger(__name__)


class CryptoBotService:
    def __init__(self):
        self.webhook_secret = settings.CRYPTOBOT_WEBHOOK_SECRET
    
    def verify_webhook_signature(self, payload: str, signature: str) -> bool:
        if not self.webhook_secret:
            return False
        
        secret = hashlib.sha256(self.webhook_secret.encode()).digest()
        expected = hmac.new(secret, payload.encode(), hashlib.sha256).hexdigest()
        
        return hmac.compare_digest(expected, signature)
