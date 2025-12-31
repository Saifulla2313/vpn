import logging
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from app.database.crud.user import get_user_by_telegram_id
from app.database.crud.subscription import get_subscription_by_user_id
from app.database.models import SubscriptionStatus
from app.keyboards.inline import get_back_keyboard
from app.localization.texts import get_text

logger = logging.getLogger(__name__)
router = Router()


def format_status(status: SubscriptionStatus) -> str:
    status_map = {
        SubscriptionStatus.ACTIVE: "✅ Активна",
        SubscriptionStatus.INACTIVE: "❌ Неактивна",
        SubscriptionStatus.EXPIRED: "⏰ Истекла",
        SubscriptionStatus.TRIAL: "🎁 Пробный период"
    }
    return status_map.get(status, "❓ Неизвестно")


@router.message(Command("profile"))
async def cmd_profile(message: Message, db: AsyncSession):
    user = await get_user_by_telegram_id(db, message.from_user.id)
    if not user:
        await message.answer("Ошибка: пользователь не найден. Нажмите /start")
        return
    
    subscription = await get_subscription_by_user_id(db, user.id)
    
    expires = "—"
    status = "❌ Неактивна"
    days_paid = 0
    
    if subscription:
        if subscription.expires_at:
            expires = subscription.expires_at.strftime("%d.%m.%Y %H:%M")
        status = format_status(subscription.status)
        days_paid = subscription.days_paid or 0
    
    text = get_text(
        "profile",
        telegram_id=user.telegram_id,
        balance=user.balance,
        expires=expires,
        status=status,
        days_paid=days_paid
    )
    
    await message.answer(text, reply_markup=get_back_keyboard(), parse_mode="HTML")


@router.callback_query(F.data == "profile")
async def callback_profile(callback: CallbackQuery, db: AsyncSession):
    user = await get_user_by_telegram_id(db, callback.from_user.id)
    if not user:
        await callback.answer("Ошибка: пользователь не найден", show_alert=True)
        return
    
    subscription = await get_subscription_by_user_id(db, user.id)
    
    expires = "—"
    status = "❌ Неактивна"
    days_paid = 0
    
    if subscription:
        if subscription.expires_at:
            expires = subscription.expires_at.strftime("%d.%m.%Y %H:%M")
        status = format_status(subscription.status)
        days_paid = subscription.days_paid or 0
    
    text = get_text(
        "profile",
        telegram_id=user.telegram_id,
        balance=user.balance,
        expires=expires,
        status=status,
        days_paid=days_paid
    )
    
    await callback.message.edit_text(text, reply_markup=get_back_keyboard(), parse_mode="HTML")
    await callback.answer()
