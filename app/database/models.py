from datetime import datetime
from enum import Enum as PyEnum
from sqlalchemy import Column, Integer, BigInteger, String, Float, DateTime, Boolean, Text, Enum, ForeignKey, Table, JSON
from sqlalchemy.orm import relationship
from app.database.database import Base


class SubscriptionStatus(str, PyEnum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    EXPIRED = "expired"
    TRIAL = "trial"


class TransactionType(str, PyEnum):
    DEPOSIT = "deposit"
    SUBSCRIPTION = "subscription"
    REFUND = "refund"
    BONUS = "bonus"


class TransactionStatus(str, PyEnum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class PromoCodeType(str, PyEnum):
    BALANCE = "balance"
    SUBSCRIPTION_DAYS = "subscription_days"
    TRIAL_SUBSCRIPTION = "trial_subscription"
    PROMO_GROUP = "promo_group"


class TicketStatus(str, PyEnum):
    OPEN = "open"
    ANSWERED = "answered"
    CLOSED = "closed"
    PENDING = "pending"
    IN_PROGRESS = "in_progress"


class WithdrawalRequestStatus(str, PyEnum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class PaymentMethodType(str, PyEnum):
    YOOKASSA = "yookassa"
    MULENPAY = "mulenpay"
    CRYPTOBOT = "cryptobot"
    PAL24 = "pal24"
    WATA = "wata"
    HELEKET = "heleket"
    PLATEGA = "platega"
    SUPPORT = "support"
    BALANCE = "balance"


PaymentMethod = PaymentMethodType


class UserStatus(str, PyEnum):
    ACTIVE = "active"
    BLOCKED = "blocked"
    DELETED = "deleted"
    SUSPENDED = "suspended"


server_squad_promo_groups = Table(
    'server_squad_promo_groups',
    Base.metadata,
    Column('server_squad_id', Integer, ForeignKey('server_squads.id'), primary_key=True),
    Column('promo_group_id', Integer, ForeignKey('promo_groups.id'), primary_key=True)
)


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(BigInteger, unique=True, index=True, nullable=False)
    username = Column(String(100), nullable=True)
    first_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=True)
    language_code = Column(String(10), default="ru")
    
    balance = Column(Float, default=0.0)
    total_spent = Column(Float, default=0.0)
    purchase_count = Column(Integer, default=0)
    total_traffic = Column(BigInteger, default=0)
    
    status = Column(String(20), default="active")
    is_admin = Column(Boolean, default=False)
    is_blocked = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    
    last_activity = Column(DateTime, nullable=True)
    
    referrer_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    referral_bonus = Column(Float, default=0.0)
    
    remnawave_uuid = Column(String(100), nullable=True)
    remnawave_short_uuid = Column(String(50), nullable=True)
    
    trial_used = Column(Boolean, default=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    subscription = relationship("Subscription", back_populates="user", uselist=False)
    transactions = relationship("Transaction", back_populates="user")

    @property
    def full_name(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.first_name or self.username or str(self.telegram_id)

    def get_primary_promo_group(self):
        return None


class Subscription(Base):
    __tablename__ = "subscriptions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    
    status = Column(Enum(SubscriptionStatus), default=SubscriptionStatus.INACTIVE)
    expires_at = Column(DateTime, nullable=True)
    
    auto_renew = Column(Boolean, default=True)
    daily_price = Column(Float, default=6.0)
    
    last_charge_date = Column(DateTime, nullable=True)
    days_paid = Column(Integer, default=0)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = relationship("User", back_populates="subscription")


class Transaction(Base):
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    type = Column(Enum(TransactionType), nullable=False)
    status = Column(Enum(TransactionStatus), default=TransactionStatus.PENDING)
    
    amount = Column(Float, nullable=False)
    currency = Column(String(10), default="RUB")
    description = Column(Text, nullable=True)
    
    payment_id = Column(String(100), nullable=True)
    payment_method = Column(String(50), nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    
    user = relationship("User", back_populates="transactions")


class PromoGroup(Base):
    __tablename__ = "promo_groups"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    priority = Column(Integer, default=0)
    server_discount_percent = Column(Integer, default=0)
    traffic_discount_percent = Column(Integer, default=0)
    device_discount_percent = Column(Integer, default=0)
    period_discounts = Column(JSON, default=dict)
    auto_assign_total_spent_kopeks = Column(Integer, nullable=True)
    apply_discounts_to_addons = Column(Boolean, default=True)
    is_default = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    promo_codes = relationship("PromoCode", back_populates="promo_group")

    def get_discount_percent(self, category, period_days):
        return 0


class PromoCode(Base):
    __tablename__ = "promo_codes"
    
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(50), unique=True, nullable=False)
    type = Column(String(50), default="balance")
    
    bonus_amount = Column(Float, default=0.0)
    bonus_days = Column(Integer, default=0)
    balance_bonus_kopeks = Column(Integer, default=0)
    subscription_days = Column(Integer, default=0)
    
    promo_group_id = Column(Integer, ForeignKey("promo_groups.id"), nullable=True)
    
    max_uses = Column(Integer, default=1)
    current_uses = Column(Integer, default=0)
    first_purchase_only = Column(Boolean, default=False)
    
    is_active = Column(Boolean, default=True)
    valid_from = Column(DateTime, default=datetime.utcnow)
    valid_until = Column(DateTime, nullable=True)
    expires_at = Column(DateTime, nullable=True)
    
    created_by = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    promo_group = relationship("PromoGroup", back_populates="promo_codes")
    uses = relationship("PromoCodeUse", back_populates="promo_code")


class PromoCodeUse(Base):
    __tablename__ = "promo_code_uses"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    promo_code_id = Column(Integer, ForeignKey("promo_codes.id"), nullable=False)
    used_at = Column(DateTime, default=datetime.utcnow)
    
    promo_code = relationship("PromoCode", back_populates="uses")


class SystemSettings(Base):
    __tablename__ = "system_settings"
    
    id = Column(Integer, primary_key=True, index=True)
    key = Column(String(100), unique=True, nullable=False)
    value = Column(Text, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


SystemSetting = SystemSettings


class ReferralEarning(Base):
    __tablename__ = "referral_earnings"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    referrer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    amount_kopeks = Column(Integer, default=0)
    source = Column(String(50), nullable=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class WithdrawalRequest(Base):
    __tablename__ = "withdrawal_requests"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    amount_kopeks = Column(Integer, nullable=False)
    status = Column(String(50), default=WithdrawalRequestStatus.PENDING.value)
    payment_method = Column(String(100), nullable=True)
    payment_details = Column(Text, nullable=True)
    admin_id = Column(Integer, nullable=True)
    admin_comment = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    processed_at = Column(DateTime, nullable=True)


class Squad(Base):
    __tablename__ = "squads"
    
    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String(100), unique=True, nullable=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class ServerSquad(Base):
    __tablename__ = "server_squads"
    
    id = Column(Integer, primary_key=True, index=True)
    squad_uuid = Column(String(100), nullable=False)
    display_name = Column(String(100), nullable=False)
    original_name = Column(String(100), nullable=True)
    country_code = Column(String(10), nullable=True)
    price_kopeks = Column(Integer, default=0)
    description = Column(Text, nullable=True)
    is_available = Column(Boolean, default=True)
    is_trial_eligible = Column(Boolean, default=False)
    sort_order = Column(Integer, default=0)
    max_users = Column(Integer, nullable=True)
    current_users = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    promo_groups = relationship(
        "PromoGroup",
        secondary=server_squad_promo_groups,
        backref="server_squads"
    )


class ServiceRule(Base):
    __tablename__ = "service_rules"
    
    id = Column(Integer, primary_key=True, index=True)
    rule_type = Column(String(100), nullable=False)
    rule_value = Column(Text, nullable=True)
    description = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class MonitoringLog(Base):
    __tablename__ = "monitoring_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    event_type = Column(String(100), nullable=False)
    message = Column(Text, nullable=True)
    level = Column(String(20), default="info")
    extra_data = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class SubscriptionConversion(Base):
    __tablename__ = "subscription_conversions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    subscription_id = Column(Integer, ForeignKey("subscriptions.id"), nullable=True)
    from_status = Column(String(50), nullable=True)
    to_status = Column(String(50), nullable=True)
    amount_kopeks = Column(Integer, default=0)
    converted_at = Column(DateTime, default=datetime.utcnow)


class SentNotification(Base):
    __tablename__ = "sent_notifications"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    message_id = Column(Integer, nullable=True)
    notification_type = Column(String(100), nullable=True)
    sent_at = Column(DateTime, default=datetime.utcnow)


class BroadcastHistory(Base):
    __tablename__ = "broadcast_history"
    
    id = Column(Integer, primary_key=True, index=True)
    target_type = Column(String(50), nullable=False)
    message_text = Column(Text, nullable=True)
    has_media = Column(Boolean, default=False)
    media_type = Column(String(50), nullable=True)
    media_file_id = Column(String(255), nullable=True)
    media_caption = Column(Text, nullable=True)
    total_count = Column(Integer, default=0)
    sent_count = Column(Integer, default=0)
    failed_count = Column(Integer, default=0)
    status = Column(String(50), default="pending")
    admin_id = Column(Integer, nullable=True)
    admin_name = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)


class SubscriptionServer(Base):
    __tablename__ = "subscription_servers"
    
    id = Column(Integer, primary_key=True, index=True)
    subscription_id = Column(Integer, ForeignKey("subscriptions.id"), nullable=False)
    server_squad_id = Column(Integer, ForeignKey("server_squads.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class UserMessage(Base):
    __tablename__ = "user_messages"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    message_text = Column(Text, nullable=True)
    is_from_admin = Column(Boolean, default=False)
    admin_id = Column(Integer, nullable=True)
    message_id = Column(Integer, nullable=True)
    has_media = Column(Boolean, default=False)
    media_type = Column(String(50), nullable=True)
    media_file_id = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class YooKassaPayment(Base):
    __tablename__ = "yookassa_payments"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    payment_id = Column(String(100), unique=True, nullable=False)
    amount_kopeks = Column(Integer, nullable=False)
    currency = Column(String(10), default="RUB")
    status = Column(String(50), default="pending")
    description = Column(Text, nullable=True)
    confirmation_url = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    paid_at = Column(DateTime, nullable=True)


class CryptoBotPayment(Base):
    __tablename__ = "cryptobot_payments"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    invoice_id = Column(String(100), unique=True, nullable=False)
    amount = Column(Float, nullable=False)
    currency = Column(String(20), default="USDT")
    status = Column(String(50), default="pending")
    description = Column(Text, nullable=True)
    pay_url = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    paid_at = Column(DateTime, nullable=True)


class MulenPayPayment(Base):
    __tablename__ = "mulenpay_payments"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    payment_id = Column(String(100), unique=True, nullable=False)
    amount_kopeks = Column(Integer, nullable=False)
    currency = Column(String(10), default="RUB")
    status = Column(String(50), default="pending")
    description = Column(Text, nullable=True)
    payment_url = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    paid_at = Column(DateTime, nullable=True)


class Pal24Payment(Base):
    __tablename__ = "pal24_payments"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    payment_id = Column(String(100), unique=True, nullable=False)
    amount_kopeks = Column(Integer, nullable=False)
    currency = Column(String(10), default="RUB")
    status = Column(String(50), default="pending")
    description = Column(Text, nullable=True)
    payment_url = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    paid_at = Column(DateTime, nullable=True)


class WataPayment(Base):
    __tablename__ = "wata_payments"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    payment_id = Column(String(100), unique=True, nullable=False)
    amount_kopeks = Column(Integer, nullable=False)
    currency = Column(String(10), default="RUB")
    status = Column(String(50), default="pending")
    description = Column(Text, nullable=True)
    payment_url = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    paid_at = Column(DateTime, nullable=True)


class HeleketPayment(Base):
    __tablename__ = "heleket_payments"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    payment_id = Column(String(100), unique=True, nullable=False)
    amount_kopeks = Column(Integer, nullable=False)
    currency = Column(String(10), default="RUB")
    status = Column(String(50), default="pending")
    description = Column(Text, nullable=True)
    payment_url = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    paid_at = Column(DateTime, nullable=True)


class PlategaPayment(Base):
    __tablename__ = "platega_payments"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    payment_id = Column(String(100), unique=True, nullable=False)
    amount_kopeks = Column(Integer, nullable=False)
    currency = Column(String(10), default="RUB")
    status = Column(String(50), default="pending")
    description = Column(Text, nullable=True)
    payment_url = Column(Text, nullable=True)
    method = Column(String(50), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    paid_at = Column(DateTime, nullable=True)


class WelcomeText(Base):
    __tablename__ = "welcome_texts"
    
    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, nullable=False)
    is_active = Column(Boolean, default=True)
    is_enabled = Column(Boolean, default=True)
    created_by = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class AdvertisingCampaign(Base):
    __tablename__ = "advertising_campaigns"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    start_parameter = Column(String(64), unique=True, nullable=False)
    bonus_type = Column(String(50), default="balance")
    balance_bonus_kopeks = Column(Integer, default=0)
    subscription_duration_days = Column(Integer, nullable=True)
    subscription_traffic_gb = Column(Integer, nullable=True)
    subscription_device_limit = Column(Integer, nullable=True)
    subscription_squads = Column(JSON, default=list)
    is_active = Column(Boolean, default=True)
    created_by = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class AdvertisingCampaignRegistration(Base):
    __tablename__ = "advertising_campaign_registrations"
    
    id = Column(Integer, primary_key=True, index=True)
    campaign_id = Column(Integer, ForeignKey("advertising_campaigns.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    registered_at = Column(DateTime, default=datetime.utcnow)


class Ticket(Base):
    __tablename__ = "tickets"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(255), nullable=False)
    status = Column(String(50), default=TicketStatus.OPEN.value)
    priority = Column(String(50), default="normal")
    is_user_reply_blocked = Column(Boolean, default=False)
    user_reply_block_permanent = Column(Boolean, default=False)
    user_reply_block_until = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    closed_at = Column(DateTime, nullable=True)
    
    user = relationship("User")
    messages = relationship("TicketMessage", back_populates="ticket")

    @property
    def is_closed(self):
        return self.status == TicketStatus.CLOSED.value

    @property
    def status_emoji(self):
        status_emojis = {
            TicketStatus.OPEN.value: "🟢",
            TicketStatus.ANSWERED.value: "🔵",
            TicketStatus.CLOSED.value: "🔴",
            TicketStatus.PENDING.value: "🟡",
            TicketStatus.IN_PROGRESS.value: "🟠",
        }
        return status_emojis.get(self.status, "⚪")

    @property
    def priority_emoji(self):
        priority_emojis = {
            "low": "🔽",
            "normal": "➖",
            "high": "🔼",
            "urgent": "🔺",
        }
        return priority_emojis.get(self.priority, "➖")


class TicketMessage(Base):
    __tablename__ = "ticket_messages"
    
    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(Integer, ForeignKey("tickets.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    message_text = Column(Text, nullable=True)
    is_from_admin = Column(Boolean, default=False)
    has_media = Column(Boolean, default=False)
    media_type = Column(String(50), nullable=True)
    media_file_id = Column(String(255), nullable=True)
    media_caption = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    ticket = relationship("Ticket", back_populates="messages")


class SupportAuditLog(Base):
    __tablename__ = "support_audit_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    admin_id = Column(Integer, nullable=False)
    action = Column(String(100), nullable=False)
    target_type = Column(String(100), nullable=True)
    target_id = Column(Integer, nullable=True)
    details = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class DiscountOffer(Base):
    __tablename__ = "discount_offers"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    discount_percent = Column(Integer, default=0)
    discount_kopeks = Column(Integer, default=0)
    applies_to = Column(String(100), nullable=True)
    is_active = Column(Boolean, default=True)
    valid_from = Column(DateTime, nullable=True)
    valid_until = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class WebApiToken(Base):
    __tablename__ = "web_api_tokens"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    token_hash = Column(String(255), nullable=False)
    prefix = Column(String(20), nullable=False)
    description = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    expires_at = Column(DateTime, nullable=True)
    last_used_at = Column(DateTime, nullable=True)
    last_used_ip = Column(String(50), nullable=True)
    created_by = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Tariff(Base):
    __tablename__ = "tariffs"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    price_kopeks = Column(Integer, default=0)
    duration_days = Column(Integer, default=30)
    traffic_gb = Column(Integer, nullable=True)
    device_limit = Column(Integer, nullable=True)
    is_active = Column(Boolean, default=True)
    sort_order = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Poll(Base):
    __tablename__ = "polls"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    reward_enabled = Column(Boolean, default=False)
    reward_amount_kopeks = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class PollQuestion(Base):
    __tablename__ = "poll_questions"
    
    id = Column(Integer, primary_key=True, index=True)
    poll_id = Column(Integer, ForeignKey("polls.id"), nullable=False)
    text = Column(Text, nullable=False)
    order = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)


class PollOption(Base):
    __tablename__ = "poll_options"
    
    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey("poll_questions.id"), nullable=False)
    text = Column(String(500), nullable=False)
    order = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)


class PollResponse(Base):
    __tablename__ = "poll_responses"
    
    id = Column(Integer, primary_key=True, index=True)
    poll_id = Column(Integer, ForeignKey("polls.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    sent_at = Column(DateTime, default=datetime.utcnow)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    reward_given = Column(Boolean, default=False)
    reward_amount_kopeks = Column(Integer, default=0)


class PollAnswer(Base):
    __tablename__ = "poll_answers"
    
    id = Column(Integer, primary_key=True, index=True)
    response_id = Column(Integer, ForeignKey("poll_responses.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("poll_questions.id"), nullable=True)
    option_id = Column(Integer, ForeignKey("poll_options.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class ContestTemplate(Base):
    __tablename__ = "contest_templates"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    prize_description = Column(Text, nullable=True)
    prize_amount_kopeks = Column(Integer, default=0)
    max_participants = Column(Integer, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class PinnedMessage(Base):
    __tablename__ = "pinned_messages"
    
    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(BigInteger, nullable=True)
    message_id = Column(Integer, nullable=True)
    message_text = Column(Text, nullable=True)
    pinned_by = Column(Integer, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class SubscriptionEvent(Base):
    __tablename__ = "subscription_events"
    
    id = Column(Integer, primary_key=True, index=True)
    event_type = Column(String(100), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    subscription_id = Column(Integer, ForeignKey("subscriptions.id"), nullable=True)
    transaction_id = Column(Integer, ForeignKey("transactions.id"), nullable=True)
    amount_kopeks = Column(Integer, nullable=True)
    currency = Column(String(16), nullable=True)
    message = Column(Text, nullable=True)
    occurred_at = Column(DateTime, default=datetime.utcnow)
    extra = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow)


class PaymentMethodConfig(Base):
    __tablename__ = "payment_methods"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    code = Column(String(50), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    min_amount_kopeks = Column(Integer, default=0)
    max_amount_kopeks = Column(Integer, nullable=True)
    commission_percent = Column(Float, default=0.0)
    sort_order = Column(Integer, default=0)
    settings = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class SubscriptionTemporaryAccess(Base):
    __tablename__ = "subscription_temporary_access"
    
    id = Column(Integer, primary_key=True, index=True)
    subscription_id = Column(Integer, ForeignKey("subscriptions.id"), nullable=True)
    offer_id = Column(Integer, ForeignKey("discount_offers.id"), nullable=True)
    squad_uuid = Column(String(100), nullable=True)
    is_active = Column(Boolean, default=True)
    expires_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    subscription = relationship("Subscription", backref="temporary_accesses")
    offer = relationship("DiscountOffer", backref="temporary_accesses")


class FaqPage(Base):
    __tablename__ = "faq_pages"
    
    id = Column(Integer, primary_key=True, index=True)
    language = Column(String(10), default="ru")
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=True)
    sort_order = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class FaqSetting(Base):
    __tablename__ = "faq_settings"
    
    id = Column(Integer, primary_key=True, index=True)
    language = Column(String(10), unique=True, nullable=False)
    is_enabled = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class UserPromoGroup(Base):
    __tablename__ = "user_promo_groups"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    group_name = Column(String(100), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = relationship("User", backref="promo_groups")


class PrivacyPolicy(Base):
    __tablename__ = "privacy_policies"
    
    id = Column(Integer, primary_key=True, index=True)
    language = Column(String(10), default="ru")
    content = Column(Text, nullable=True)
    is_enabled = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class PromoOfferTemplate(Base):
    __tablename__ = "promo_offer_templates"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    offer_type = Column(String(50), default="discount")
    discount_percent = Column(Float, default=0.0)
    discount_amount_kopeks = Column(Integer, default=0)
    duration_hours = Column(Integer, default=24)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class PromoOfferLog(Base):
    __tablename__ = "promo_offer_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    template_id = Column(Integer, ForeignKey("promo_offer_templates.id"), nullable=True)
    offer_type = Column(String(50), nullable=True)
    action = Column(String(50), nullable=True)
    status = Column(String(50), default="sent")
    details = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", backref="promo_logs")
    template = relationship("PromoOfferTemplate", backref="logs")


class PublicOffer(Base):
    __tablename__ = "public_offers"
    
    id = Column(Integer, primary_key=True, index=True)
    language = Column(String(10), default="ru")
    content = Column(Text, nullable=True)
    is_enabled = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
