import os
from typing import List, Optional
from dataclasses import dataclass, field


@dataclass
class Settings:
    # Bot settings
    BOT_TOKEN: str = field(default_factory=lambda: os.getenv("BOT_TOKEN", ""))
    ADMIN_IDS: List[int] = field(default_factory=list)
    
    # Database
    DATABASE_URL: str = field(default_factory=lambda: os.getenv("DATABASE_URL", ""))
    
    # Remnawave
    REMNAWAVE_URL: str = field(default_factory=lambda: os.getenv("REMNAWAVE_URL", ""))
    REMNAWAVE_API_KEY: str = field(default_factory=lambda: os.getenv("REMNAWAVE_API_KEY", ""))
    REMNAWAVE_SECRET_KEY: Optional[str] = field(default_factory=lambda: os.getenv("REMNAWAVE_SECRET_KEY"))
    
    # YooKassa
    YOOKASSA_SHOP_ID: str = field(default_factory=lambda: os.getenv("YOOKASSA_SHOP_ID", ""))
    YOOKASSA_SECRET_KEY: str = field(default_factory=lambda: os.getenv("YOOKASSA_SECRET_KEY", ""))
    YOOKASSA_RETURN_URL: Optional[str] = field(default_factory=lambda: os.getenv("YOOKASSA_RETURN_URL"))
    YOOKASSA_DEFAULT_RECEIPT_EMAIL: str = field(default_factory=lambda: os.getenv("YOOKASSA_DEFAULT_RECEIPT_EMAIL", "noreply@vpn.bot"))
    YOOKASSA_VAT_CODE: int = 1
    YOOKASSA_PAYMENT_MODE: str = "full_payment"
    YOOKASSA_PAYMENT_SUBJECT: str = "service"
    
    # Subscription pricing (rubles per day)
    SUBSCRIPTION_DAILY_PRICE: float = 6.0
    
    # Web API
    WEB_API_TITLE: str = "VPN Bot Admin API"
    WEB_API_VERSION: str = "1.0.0"
    WEB_API_REQUEST_LOGGING: bool = True
    WEB_API_DOCS_ENABLED: bool = True
    WEB_API_ALLOWED_ORIGINS: str = field(default_factory=lambda: os.getenv("WEB_API_ALLOWED_ORIGINS", "*"))
    
    # Webhook settings
    TRIBUTE_ENABLED: bool = False
    TRIBUTE_API_KEY: str = ""
    TRIBUTE_WEBHOOK_HOST: str = "0.0.0.0"
    TRIBUTE_WEBHOOK_PORT: int = 8080
    TRIBUTE_WEBHOOK_PATH: str = "/webhook/tribute"
    CRYPTOBOT_WEBHOOK_PATH: str = "/webhook/cryptobot"
    MULENPAY_WEBHOOK_PATH: str = "/webhook/mulenpay"
    MULENPAY_SECRET_KEY: str = ""
    CRYPTOBOT_WEBHOOK_SECRET: str = ""
    
    # Trial settings
    TRIAL_DAYS: int = field(default_factory=lambda: int(os.getenv("TRIAL_DAYS", "1")))
    TRIAL_TRAFFIC_GB: int = field(default_factory=lambda: int(os.getenv("TRIAL_TRAFFIC_GB", "10")))
    TRIAL_ENABLED: bool = field(default_factory=lambda: os.getenv("TRIAL_ENABLED", "true").lower() == "true")
    
    # RemnaWave default internal squad UUID (used for new subscriptions)
    REMNAWAVE_DEFAULT_SQUAD_UUID: str = field(default_factory=lambda: os.getenv("REMNAWAVE_DEFAULT_SQUAD_UUID", ""))
    
    # Default device limit for new users (HWID limit)
    DEFAULT_DEVICE_LIMIT: int = field(default_factory=lambda: int(os.getenv("DEFAULT_DEVICE_LIMIT", "1")))
    
    # Maintenance
    MAINTENANCE_MODE: bool = False
    
    def __post_init__(self):
        admin_ids_str = os.getenv("ADMIN_IDS", "")
        if admin_ids_str:
            self.ADMIN_IDS = [int(x.strip()) for x in admin_ids_str.split(",") if x.strip().isdigit()]
    
    def is_admin(self, user_id: int) -> bool:
        return user_id in self.ADMIN_IDS
    
    def is_cryptobot_enabled(self) -> bool:
        return bool(self.CRYPTOBOT_WEBHOOK_SECRET)
    
    def is_mulenpay_enabled(self) -> bool:
        return bool(self.MULENPAY_SECRET_KEY)
    
    def get_mulenpay_display_name(self) -> str:
        return "MulenPay"
    
    def get_web_api_docs_config(self) -> dict:
        if self.WEB_API_DOCS_ENABLED:
            return {
                "docs_url": "/docs",
                "redoc_url": "/redoc",
                "openapi_url": "/openapi.json"
            }
        return {
            "docs_url": None,
            "redoc_url": None,
            "openapi_url": None
        }
    
    def get_web_api_allowed_origins(self) -> List[str]:
        if self.WEB_API_ALLOWED_ORIGINS == "*":
            return ["*"]
        return [o.strip() for o in self.WEB_API_ALLOWED_ORIGINS.split(",")]


settings = Settings()
