from datetime import datetime
from enum import Enum as PyEnum
from sqlalchemy import Column, Integer, BigInteger, String, Float, DateTime, Boolean, Text, Enum, ForeignKey
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


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(BigInteger, unique=True, index=True, nullable=False)
    username = Column(String(100), nullable=True)
    first_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=True)
    language_code = Column(String(10), default="ru")
    
    balance = Column(Float, default=0.0)
    
    is_admin = Column(Boolean, default=False)
    is_blocked = Column(Boolean, default=False)
    
    referrer_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    referral_bonus = Column(Float, default=0.0)
    
    remnawave_uuid = Column(String(100), nullable=True)
    remnawave_short_uuid = Column(String(50), nullable=True)
    
    trial_used = Column(Boolean, default=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    subscription = relationship("Subscription", back_populates="user", uselist=False)
    transactions = relationship("Transaction", back_populates="user")


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


class PromoCode(Base):
    __tablename__ = "promo_codes"
    
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(50), unique=True, nullable=False)
    
    bonus_amount = Column(Float, default=0.0)
    bonus_days = Column(Integer, default=0)
    
    max_uses = Column(Integer, default=1)
    current_uses = Column(Integer, default=0)
    
    is_active = Column(Boolean, default=True)
    expires_at = Column(DateTime, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)


class SystemSettings(Base):
    __tablename__ = "system_settings"
    
    id = Column(Integer, primary_key=True, index=True)
    key = Column(String(100), unique=True, nullable=False)
    value = Column(Text, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
