import logging
from datetime import datetime, timedelta
from aiogram import Router, F
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.crud.user import get_user_by_telegram_id, update_user_remnawave, mark_trial_used
from app.database.crud.subscription import (
    get_subscription_by_user_id,
    activate_subscription,
    set_trial_subscription
)
from app.database.models import SubscriptionStatus
from app.keyboards.inline import get_subscription_keyboard, get_back_keyboard
from app.localization.texts import get_text
from app.config import settings
from app.remnawave_api import RemnaWaveAPI, UserStatus

logger = logging.getLogger(__name__)
router = Router()


async def create_remnawave_user(user, db: AsyncSession) -> dict:
    if not settings.REMNAWAVE_URL or not settings.REMNAWAVE_API_KEY:
        return None
    
    try:
        async with RemnaWaveAPI(
            settings.REMNAWAVE_URL,
            settings.REMNAWAVE_API_KEY,
            settings.REMNAWAVE_SECRET_KEY
        ) as api:
            username = f"tg_{user.telegram_id}"
            
            existing = await api.get_user_by_telegram_id(user.telegram_id)
            if existing:
                rw_user = existing[0]
                await update_user_remnawave(db, user.id, rw_user.uuid, rw_user.short_uuid)
                return {
                    "uuid": rw_user.uuid,
                    "short_uuid": rw_user.short_uuid,
                    "subscription_url": rw_user.subscription_url
                }
            
            expire_at = datetime.utcnow() + timedelta(days=1)
            rw_user = await api.create_user(
                username=username,
                expire_at=expire_at,
                status=UserStatus.ACTIVE,
                telegram_id=user.telegram_id
            )
            
            await update_user_remnawave(db, user.id, rw_user.uuid, rw_user.short_uuid)
            
            return {
                "uuid": rw_user.uuid,
                "short_uuid": rw_user.short_uuid,
                "subscription_url": rw_user.subscription_url
            }
    except Exception as e:
        logger.error(f"Error creating Remnawave user: {e}")
        return None


async def update_remnawave_subscription(user, days: int) -> bool:
    if not settings.REMNAWAVE_URL or not settings.REMNAWAVE_API_KEY:
        return False
    
    if not user.remnawave_uuid:
        return False
    
    try:
        async with RemnaWaveAPI(
            settings.REMNAWAVE_URL,
            settings.REMNAWAVE_API_KEY,
            settings.REMNAWAVE_SECRET_KEY
        ) as api:
            expire_at = datetime.utcnow() + timedelta(days=days)
            await api.update_user(
                uuid=user.remnawave_uuid,
                expire_at=expire_at,
                status=UserStatus.ACTIVE
            )
            return True
    except Exception as e:
        logger.error(f"Error updating Remnawave subscription: {e}")
        return False


async def disable_remnawave_user(user) -> bool:
    if not settings.REMNAWAVE_URL or not settings.REMNAWAVE_API_KEY:
        return False
    
    if not user.remnawave_uuid:
        return False
    
    try:
        async with RemnaWaveAPI(
            settings.REMNAWAVE_URL,
            settings.REMNAWAVE_API_KEY,
            settings.REMNAWAVE_SECRET_KEY
        ) as api:
            await api.disable_user(user.remnawave_uuid)
            return True
    except Exception as e:
        logger.error(f"Error disabling Remnawave user: {e}")
        return False


@router.callback_query(F.data == "subscription")
async def callback_subscription(callback: CallbackQuery, db: AsyncSession):
    user = await get_user_by_telegram_id(db, callback.from_user.id)
    if not user:
        await callback.answer("Ошибка: пользователь не найден", show_alert=True)
        return
    
    subscription = await get_subscription_by_user_id(db, user.id)
    has_active = subscription and subscription.status in [SubscriptionStatus.ACTIVE, SubscriptionStatus.TRIAL]
    
    if has_active:
        expires = subscription.expires_at.strftime("%d.%m.%Y %H:%M") if subscription.expires_at else "—"
        text = get_text(
            "subscription_active",
            expires=expires,
            balance=user.balance
        )
    else:
        text = get_text(
            "subscription_inactive",
            balance=user.balance
        )
    
    await callback.message.edit_text(
        text,
        reply_markup=get_subscription_keyboard(has_active),
        parse_mode="HTML"
    )
    await callback.answer()


@router.callback_query(F.data == "activate_trial")
async def callback_activate_trial(callback: CallbackQuery, db: AsyncSession):
    user = await get_user_by_telegram_id(db, callback.from_user.id)
    if not user:
        await callback.answer("Ошибка: пользователь не найден", show_alert=True)
        return
    
    if user.trial_used:
        await callback.message.edit_text(
            get_text("trial_already_used"),
            reply_markup=get_back_keyboard(),
            parse_mode="HTML"
        )
        await callback.answer()
        return
    
    rw_data = await create_remnawave_user(user, db)
    await set_trial_subscription(db, user.id, days=settings.TRIAL_DAYS)
    await mark_trial_used(db, user.id)
    
    await callback.message.edit_text(
        get_text("trial_activated"),
        reply_markup=get_subscription_keyboard(True),
        parse_mode="HTML"
    )
    await callback.answer("Пробный период активирован!")


@router.callback_query(F.data == "get_key")
async def callback_get_key(callback: CallbackQuery, db: AsyncSession):
    user = await get_user_by_telegram_id(db, callback.from_user.id)
    if not user:
        await callback.answer("Ошибка: пользователь не найден", show_alert=True)
        return
    
    if not user.remnawave_uuid:
        rw_data = await create_remnawave_user(user, db)
        if not rw_data:
            await callback.answer("Ошибка создания ключа. Попробуйте позже.", show_alert=True)
            return
        subscription_url = rw_data["subscription_url"]
    else:
        try:
            async with RemnaWaveAPI(
                settings.REMNAWAVE_URL,
                settings.REMNAWAVE_API_KEY,
                settings.REMNAWAVE_SECRET_KEY
            ) as api:
                info = await api.get_subscription_info(user.remnawave_short_uuid)
                subscription_url = info.subscription_url
        except Exception as e:
            logger.error(f"Error getting subscription info: {e}")
            await callback.answer("Ошибка получения ключа. Попробуйте позже.", show_alert=True)
            return
    
    text = get_text(
        "vpn_key",
        key=subscription_url,
        subscription_url=subscription_url
    )
    
    await callback.message.edit_text(
        text,
        reply_markup=get_back_keyboard(),
        parse_mode="HTML"
    )
    await callback.answer()


@router.callback_query(F.data == "refresh_key")
async def callback_refresh_key(callback: CallbackQuery, db: AsyncSession):
    user = await get_user_by_telegram_id(db, callback.from_user.id)
    if not user or not user.remnawave_uuid:
        await callback.answer("Ключ не найден", show_alert=True)
        return
    
    try:
        async with RemnaWaveAPI(
            settings.REMNAWAVE_URL,
            settings.REMNAWAVE_API_KEY,
            settings.REMNAWAVE_SECRET_KEY
        ) as api:
            await api.revoke_user_subscription(user.remnawave_uuid)
            rw_user = await api.get_user_by_uuid(user.remnawave_uuid)
            await update_user_remnawave(db, user.id, rw_user.uuid, rw_user.short_uuid)
            
            info = await api.get_subscription_info(rw_user.short_uuid)
            subscription_url = info.subscription_url
    except Exception as e:
        logger.error(f"Error refreshing key: {e}")
        await callback.answer("Ошибка обновления ключа", show_alert=True)
        return
    
    text = get_text(
        "vpn_key",
        key=subscription_url,
        subscription_url=subscription_url
    )
    
    await callback.message.edit_text(
        text,
        reply_markup=get_back_keyboard(),
        parse_mode="HTML"
    )
    await callback.answer("Ключ обновлен!")
