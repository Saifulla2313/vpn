import os
import logging
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.crud.user import get_user_by_telegram_id, create_user
from app.keyboards.inline import get_main_menu_keyboard, get_not_opening_menu_keyboard
from app.localization.texts import get_text
from app.config import settings

logger = logging.getLogger(__name__)
router = Router()


def get_webapp_url() -> str:
    domain = os.getenv("REPLIT_DEV_DOMAIN", "")
    if domain:
        return f"https://{domain}/miniapp"
    return None


@router.message(CommandStart())
async def cmd_start(message: Message, db: AsyncSession):
    telegram_id = message.from_user.id
    
    user = await get_user_by_telegram_id(db, telegram_id)
    
    if not user:
        referrer_id = None
        if message.text and len(message.text.split()) > 1:
            try:
                ref_param = message.text.split()[1]
                if ref_param.startswith("ref"):
                    referrer_id = int(ref_param[3:])
            except (ValueError, IndexError):
                pass
        
        user = await create_user(
            db,
            telegram_id=telegram_id,
            username=message.from_user.username,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name,
            language_code=message.from_user.language_code or "ru",
            referrer_id=referrer_id
        )
        logger.info(f"New user registered: {telegram_id}")
        
        from app.database.crud.user import update_user_balance
        from app.remnawave_api import RemnaWaveAPI
        from datetime import datetime, timedelta
        
        WELCOME_BONUS = 50.0
        await update_user_balance(db, user.id, WELCOME_BONUS)
        logger.info(f"Added welcome bonus {WELCOME_BONUS}₽ to user {telegram_id}")
        
        try:
            async with RemnaWaveAPI(base_url=settings.REMNAWAVE_URL, api_key=settings.REMNAWAVE_API_KEY) as api:
                expire_at = datetime.utcnow() + timedelta(days=1)
                
                active_squads = None
                if settings.REMNAWAVE_DEFAULT_SQUAD_UUID:
                    active_squads = [settings.REMNAWAVE_DEFAULT_SQUAD_UUID]
                
                remnawave_user = await api.create_user(
                    telegram_id=telegram_id,
                    username=message.from_user.username or f"user_{telegram_id}",
                    expire_at=expire_at,
                    traffic_limit_bytes=0,
                    hwid_device_limit=settings.DEFAULT_DEVICE_LIMIT,
                    active_internal_squads=active_squads
                )
                
                if remnawave_user:
                    user.remnawave_uuid = remnawave_user.uuid
                    await db.commit()
                    logger.info(f"Subscription created for new user {telegram_id}, balance: {WELCOME_BONUS}₽")
        except Exception as e:
            logger.error(f"Failed to create subscription for user {telegram_id}: {e}")
    
    webapp_url = get_webapp_url()
    
    await message.answer(
        get_text("welcome"),
        reply_markup=get_main_menu_keyboard(webapp_url, user_id=telegram_id),
        parse_mode="HTML"
    )


@router.callback_query(F.data == "back_to_menu")
async def back_to_menu(callback: CallbackQuery):
    webapp_url = get_webapp_url()
    
    await callback.message.edit_text(
        get_text("welcome"),
        reply_markup=get_main_menu_keyboard(webapp_url, user_id=callback.from_user.id),
        parse_mode="HTML"
    )
    await callback.answer()


@router.callback_query(F.data == "not_opening_menu")
async def not_opening_menu(callback: CallbackQuery):
    await callback.message.edit_text(
        "📱 <b>Не открывается приложение?</b>\n\n"
        "Выберите нужный раздел ниже:",
        reply_markup=get_not_opening_menu_keyboard(),
        parse_mode="HTML"
    )
    await callback.answer()


@router.callback_query(F.data == "back_to_main")
async def back_to_main(callback: CallbackQuery):
    webapp_url = get_webapp_url()
    
    await callback.message.edit_text(
        get_text("welcome"),
        reply_markup=get_main_menu_keyboard(webapp_url, user_id=callback.from_user.id),
        parse_mode="HTML"
    )
    await callback.answer()


@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(
        get_text("help"),
        parse_mode="HTML"
    )


@router.callback_query(F.data == "help")
async def callback_help(callback: CallbackQuery):
    from app.keyboards.inline import get_back_keyboard
    
    await callback.message.edit_text(
        get_text("help"),
        reply_markup=get_back_keyboard(),
        parse_mode="HTML"
    )
    await callback.answer()
