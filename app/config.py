import os
from typing import List, Optional, Dict
from dataclasses import dataclass, field


PERIOD_PRICES: Dict[int, int] = {
    1: 600,
    7: 3500,
    30: 12000,
    90: 30000,
    180: 54000,
    365: 96000,
}


@dataclass
class Settings:
    # Bot settings
    BOT_TOKEN: str = field(default_factory=lambda: os.getenv("BOT_TOKEN", ""))
    ADMIN_IDS: List[int] = field(default_factory=list)
    
    # Database
    DATABASE_URL: str = field(default_factory=lambda: os.getenv("DATABASE_URL", ""))
    
    # Redis
    REDIS_URL: Optional[str] = field(default_factory=lambda: os.getenv("REDIS_URL"))
    
    # Remnawave
    REMNAWAVE_URL: str = field(default_factory=lambda: os.getenv("REMNAWAVE_URL", ""))
    REMNAWAVE_API_KEY: str = field(default_factory=lambda: os.getenv("REMNAWAVE_API_KEY", ""))
    REMNAWAVE_SECRET_KEY: Optional[str] = field(default_factory=lambda: os.getenv("REMNAWAVE_SECRET_KEY"))
    
    # YooKassa
    YOOKASSA_SHOP_ID: str = field(default_factory=lambda: os.getenv("YOOKASSA_SHOP_ID", ""))
    YOOKASSA_SECRET_KEY: str = field(default_factory=lambda: os.getenv("YOOKASSA_SECRET_KEY", ""))
    YOOKASSA_RETURN_URL: Optional[str] = field(default_factory=lambda: os.getenv("YOOKASSA_RETURN_URL"))
    YOOKASSA_DEFAULT_RECEIPT_EMAIL: str = field(default_factory=lambda: os.getenv("YOOKASSA_DEFAULT_RECEIPT_EMAIL", "noreply@vpn.bot"))
    YOOKASSA_VAT_CODE: int = field(default_factory=lambda: int(os.getenv("YOOKASSA_VAT_CODE", "1")))
    YOOKASSA_PAYMENT_MODE: str = field(default_factory=lambda: os.getenv("YOOKASSA_PAYMENT_MODE", "full_payment"))
    YOOKASSA_PAYMENT_SUBJECT: str = field(default_factory=lambda: os.getenv("YOOKASSA_PAYMENT_SUBJECT", "service"))
    
    # Subscription pricing (rubles per day per device)
    SUBSCRIPTION_DAILY_PRICE: float = field(default_factory=lambda: float(os.getenv("SUBSCRIPTION_DAILY_PRICE", "6.0")))
    # Device limit: 0 = unlimited
    DEVICE_LIMIT_ENABLED: bool = field(default_factory=lambda: os.getenv("DEVICE_LIMIT_ENABLED", "false").lower() == "true")
    
    # Web API
    WEB_API_ENABLED: bool = field(default_factory=lambda: os.getenv("WEB_API_ENABLED", "false").lower() == "true")
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
    
    # Backup settings
    BACKUP_LOCATION: str = field(default_factory=lambda: os.getenv("BACKUP_LOCATION", "./data/backups"))
    BACKUP_AUTO_ENABLED: bool = field(default_factory=lambda: os.getenv("BACKUP_AUTO_ENABLED", "false").lower() == "true")
    BACKUP_INTERVAL_HOURS: int = field(default_factory=lambda: int(os.getenv("BACKUP_INTERVAL_HOURS", "24")))
    BACKUP_MAX_KEEP: int = field(default_factory=lambda: int(os.getenv("BACKUP_MAX_KEEP", "7")))
    
    # Bot username for return URLs
    BOT_USERNAME: str = field(default_factory=lambda: os.getenv("BOT_USERNAME", "vpn_bot"))
    
    # Logo and branding
    LOGO_FILE: str = field(default_factory=lambda: os.getenv("LOGO_FILE", "assets/logo.png"))
    
    # Default language
    DEFAULT_LANGUAGE: str = field(default_factory=lambda: os.getenv("DEFAULT_LANGUAGE", "ru"))
    
    # Timezone
    TIMEZONE: str = field(default_factory=lambda: os.getenv("TIMEZONE", "Europe/Moscow"))
    
    # Inactive user cleanup
    INACTIVE_USER_DELETE_MONTHS: int = field(default_factory=lambda: int(os.getenv("INACTIVE_USER_DELETE_MONTHS", "6")))
    
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
    
    def is_yookassa_enabled(self) -> bool:
        return bool(self.YOOKASSA_SHOP_ID and self.YOOKASSA_SECRET_KEY)
    
    @property
    def REMNAWAVE_API_URL(self) -> str:
        """Alias for REMNAWAVE_URL for backward compatibility."""
        return self.REMNAWAVE_URL
    
    def is_remnawave_enabled(self) -> bool:
        return bool(self.REMNAWAVE_URL and self.REMNAWAVE_API_KEY)
    
    def is_heleket_enabled(self) -> bool:
        return False
    
    def is_pal24_enabled(self) -> bool:
        return False
    
    def is_wata_enabled(self) -> bool:
        return False
    
    def is_platega_enabled(self) -> bool:
        return False
    
    def is_support_topup_enabled(self) -> bool:
        return False
    
    def is_referral_program_enabled(self) -> bool:
        return False
    
    def is_devices_selection_enabled(self) -> bool:
        return False
    
    def is_maintenance_monitoring_enabled(self) -> bool:
        return False
    
    def is_trial_paid_activation_enabled(self) -> bool:
        return False
    
    def is_auto_purchase_after_topup_enabled(self) -> bool:
        return False
    
    def is_payment_verification_auto_check_enabled(self) -> bool:
        return False
    
    def is_admin_notifications_enabled(self) -> bool:
        return True
    
    def is_backup_send_enabled(self) -> bool:
        return False
    
    def is_web_api_enabled(self) -> bool:
        return bool(self.WEB_API_ENABLED)
    
    def get_platega_active_methods(self) -> List[str]:
        return []
    
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
    
    def model_dump(self) -> Dict[str, any]:
        """Return all settings as a dictionary (Pydantic compatibility)."""
        from dataclasses import fields
        return {f.name: getattr(self, f.name) for f in fields(self)}
    
    def get_remnawave_auth_params(self) -> Dict[str, str]:
        """Get RemnaWave authentication parameters."""
        return {
            "base_url": self.REMNAWAVE_URL,
            "api_key": self.REMNAWAVE_API_KEY,
            "secret_key": self.REMNAWAVE_SECRET_KEY or "",
        }
    
    def get_period_price(self, period_days: int) -> Optional[int]:
        """Get price for a subscription period."""
        return PERIOD_PRICES.get(period_days)
    
    def get_traffic_price(self, traffic_gb: int) -> Optional[int]:
        """Get price for traffic amount."""
        return TRAFFIC_PRICES.get(traffic_gb)


settings = Settings()


TRAFFIC_PRICES: Dict[int, int] = {
    10: 1000,
    50: 4000,
    100: 7000,
    500: 30000,
}


ENV_OVERRIDE_KEYS: List[str] = [
    "PERIOD_PRICES",
    "TRAFFIC_PRICES",
]


def refresh_period_prices() -> None:
    """Refresh period prices from environment or database."""
    pass


def refresh_traffic_prices() -> None:
    """Refresh traffic prices from environment or database."""
    pass
