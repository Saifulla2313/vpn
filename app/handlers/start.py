import os
import logging
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.crud.user import get_user_by_telegram_id, create_user
from app.keyboards.inline import get_main_menu_keyboard
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
