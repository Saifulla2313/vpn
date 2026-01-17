import logging
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.database.crud.user import get_user_by_telegram_id, get_all_users, update_user_balance
from app.database.crud.subscription import get_active_subscriptions
from app.database.models import User, Subscription, SubscriptionStatus
from app.keyboards.inline import get_admin_keyboard, get_back_keyboard
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from app.localization.texts import get_text
from app.config import settings

logger = logging.getLogger(__name__)
router = Router()


class AdminStates(StatesGroup):
    waiting_user_id = State()
    waiting_balance_amount = State()
    waiting_broadcast = State()
    waiting_search_user = State()
    waiting_promo_code = State()
    waiting_promo_discount = State()
    waiting_promo_uses = State()


def is_admin(user_id: int) -> bool:
    return settings.is_admin(user_id)


@router.message(Command("admin"))
async def cmd_admin(message: Message, db: AsyncSession):
    if not is_admin(message.from_user.id):
        return
    
    result = await db.execute(select(func.count(User.id)))
    users_count = result.scalar()
    
    result = await db.execute(
        select(func.count(Subscription.id)).where(
            Subscription.status == SubscriptionStatus.ACTIVE
        )
    )
    active_count = result.scalar()
    
    result = await db.execute(select(func.sum(User.balance)))
    total_balance = result.scalar() or 0.0
    
    text = get_text(
        "admin_panel",
        users_count=users_count,
        active_count=active_count,
        total_balance=total_balance
    )
    
    await message.answer(text, reply_markup=get_admin_keyboard(), parse_mode="HTML")


@router.callback_query(F.data == "admin_stats")
async def callback_admin_stats(callback: CallbackQuery, db: AsyncSession):
    if not is_admin(callback.from_user.id):
        await callback.answer("Нет доступа", show_alert=True)
        return
    
    result = await db.execute(select(func.count(User.id)))
    users_count = result.scalar()
    
    result = await db.execute(
        select(func.count(Subscription.id)).where(
            Subscription.status == SubscriptionStatus.ACTIVE
        )
    )
    active_count = result.scalar()
    
    result = await db.execute(select(func.sum(User.balance)))
    total_balance = result.scalar() or 0.0
    
    text = f"""
📊 <b>Статистика</b>

👥 Всего пользователей: <b>{users_count}</b>
✅ Активных подписок: <b>{active_count}</b>
💰 Общий баланс: <b>{total_balance:.2f}₽</b>
"""
    
    await callback.message.edit_text(text, reply_markup=get_admin_keyboard(), parse_mode="HTML")
    await callback.answer()


@router.callback_query(F.data == "admin_users")
async def callback_admin_users(callback: CallbackQuery, db: AsyncSession):
    if not is_admin(callback.from_user.id):
        await callback.answer("Нет доступа", show_alert=True)
        return
    
    users = await get_all_users(db, limit=20)
    
    text = "👥 <b>Последние пользователи:</b>\n\n"
    
    for user in users[:20]:
        status = "✅" if user.subscription and user.subscription.status == SubscriptionStatus.ACTIVE else "❌"
        text += f"{status} <code>{user.telegram_id}</code> - {user.balance:.2f}₽\n"
    
    await callback.message.edit_text(text, reply_markup=get_admin_keyboard(), parse_mode="HTML")
    await callback.answer()


@router.callback_query(F.data == "admin_add_balance")
async def callback_admin_add_balance(callback: CallbackQuery, state: FSMContext):
    if not is_admin(callback.from_user.id):
        await callback.answer("Нет доступа", show_alert=True)
        return
    
    await callback.message.edit_text(
        "Введите Telegram ID пользователя:",
        reply_markup=get_back_keyboard(),
        parse_mode="HTML"
    )
    await state.set_state(AdminStates.waiting_user_id)
    await callback.answer()


@router.message(AdminStates.waiting_user_id)
async def process_admin_user_id(message: Message, db: AsyncSession, state: FSMContext):
    if not is_admin(message.from_user.id):
        return
    
    try:
        telegram_id = int(message.text)
    except ValueError:
        await message.answer("Введите корректный ID")
        return
    
    user = await get_user_by_telegram_id(db, telegram_id)
    if not user:
        await message.answer("Пользователь не найден")
        return
    
    await state.update_data(target_user_id=user.id)
    await state.set_state(AdminStates.waiting_balance_amount)
    
    await message.answer(
        f"Пользователь найден!\nТекущий баланс: {user.balance:.2f}₽\n\nВведите сумму для пополнения:"
    )


@router.message(AdminStates.waiting_balance_amount)
async def process_admin_balance_amount(message: Message, db: AsyncSession, state: FSMContext):
    if not is_admin(message.from_user.id):
        return
    
    try:
        amount = float(message.text.replace(",", "."))
    except ValueError:
        await message.answer("Введите корректную сумму")
        return
    
    data = await state.get_data()
    user_id = data.get("target_user_id")
    
    user = await update_user_balance(db, user_id, amount)
    
    await state.clear()
    
    if user:
        await message.answer(
            f"✅ Баланс пополнен!\nНовый баланс: {user.balance:.2f}₽",
            reply_markup=get_admin_keyboard()
        )
    else:
        await message.answer("Ошибка обновления баланса")


@router.callback_query(F.data == "admin_broadcast")
async def callback_admin_broadcast(callback: CallbackQuery, state: FSMContext):
    if not is_admin(callback.from_user.id):
        await callback.answer("Нет доступа", show_alert=True)
        return
    
    await callback.message.edit_text(
        "📢 Введите текст рассылки:",
        reply_markup=get_back_keyboard(),
        parse_mode="HTML"
    )
    await state.set_state(AdminStates.waiting_broadcast)
    await callback.answer()


@router.message(AdminStates.waiting_broadcast)
async def process_admin_broadcast(message: Message, db: AsyncSession, state: FSMContext):
    if not is_admin(message.from_user.id):
        return
    
    broadcast_text = message.text
    users = await get_all_users(db, limit=10000)
    
    await state.clear()
    
    sent = 0
    failed = 0
    
    for user in users:
        try:
            await message.bot.send_message(
                user.telegram_id,
                broadcast_text,
                parse_mode="HTML"
            )
            sent += 1
        except Exception as e:
            failed += 1
            logger.error(f"Failed to send broadcast to {user.telegram_id}: {e}")
    
    await message.answer(
        f"📢 Рассылка завершена!\n\n✅ Отправлено: {sent}\n❌ Ошибок: {failed}",
        reply_markup=get_admin_keyboard()
    )


@router.callback_query(F.data == "admin_search")
async def callback_admin_search(callback: CallbackQuery, state: FSMContext):
    if not is_admin(callback.from_user.id):
        await callback.answer("Нет доступа", show_alert=True)
        return
    
    await callback.message.edit_text(
        "🔍 Введите Telegram ID или @username для поиска:",
        reply_markup=get_back_keyboard(),
        parse_mode="HTML"
    )
    await state.set_state(AdminStates.waiting_search_user)
    await callback.answer()


@router.message(AdminStates.waiting_search_user)
async def process_admin_search(message: Message, db: AsyncSession, state: FSMContext):
    if not is_admin(message.from_user.id):
        return
    
    search_query = message.text.strip()
    user = None
    
    if search_query.startswith("@"):
        username = search_query[1:]
        result = await db.execute(
            select(User).where(User.username == username)
        )
        user = result.scalar_one_or_none()
    else:
        try:
            telegram_id = int(search_query)
            user = await get_user_by_telegram_id(db, telegram_id)
        except ValueError:
            result = await db.execute(
                select(User).where(User.username == search_query)
            )
            user = result.scalar_one_or_none()
    
    await state.clear()
    
    if not user:
        await message.answer(
            "❌ Пользователь не найден",
            reply_markup=get_admin_keyboard()
        )
        return
    
    subscription = None
    if user.subscription:
        subscription = user.subscription
    
    status_emoji = "✅" if subscription and subscription.status == SubscriptionStatus.ACTIVE else "❌"
    
    text = f"""
👤 <b>Информация о пользователе</b>

🆔 ID: <code>{user.telegram_id}</code>
📛 Username: @{user.username or 'не указан'}
💰 Баланс: <b>{user.balance:.2f}₽</b>
{status_emoji} Подписка: {subscription.status.value if subscription else 'нет'}
🎁 Пробный период: {'использован' if user.trial_used else 'доступен'}
📅 Регистрация: {user.created_at.strftime('%d.%m.%Y') if user.created_at else 'неизвестно'}
"""
    
    if user.remnawave_uuid:
        text += f"\n🔑 RemnaWave UUID: <code>{user.remnawave_uuid[:8]}...</code>"
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="💰 Изменить баланс", callback_data=f"admin_edit_balance_{user.id}"),
            InlineKeyboardButton(text="🔄 Сбросить триал", callback_data=f"admin_reset_trial_{user.id}")
        ],
        [
            InlineKeyboardButton(text="⬅️ Назад", callback_data="back_admin")
        ]
    ])
    
    await message.answer(text, reply_markup=keyboard, parse_mode="HTML")


@router.callback_query(F.data.startswith("admin_edit_balance_"))
async def callback_admin_edit_balance(callback: CallbackQuery, state: FSMContext):
    if not is_admin(callback.from_user.id):
        await callback.answer("Нет доступа", show_alert=True)
        return
    
    user_id = int(callback.data.split("_")[-1])
    await state.update_data(target_user_id=user_id)
    await state.set_state(AdminStates.waiting_balance_amount)
    
    await callback.message.edit_text(
        "Введите сумму (положительную для пополнения, отрицательную для списания):",
        reply_markup=get_back_keyboard(),
        parse_mode="HTML"
    )
    await callback.answer()


@router.callback_query(F.data.startswith("admin_reset_trial_"))
async def callback_admin_reset_trial(callback: CallbackQuery, db: AsyncSession):
    if not is_admin(callback.from_user.id):
        await callback.answer("Нет доступа", show_alert=True)
        return
    
    user_id = int(callback.data.split("_")[-1])
    
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    
    if user:
        user.trial_used = False
        await db.commit()
        await callback.answer("✅ Пробный период сброшен!", show_alert=True)
    else:
        await callback.answer("❌ Пользователь не найден", show_alert=True)


@router.callback_query(F.data == "admin_promo")
async def callback_admin_promo(callback: CallbackQuery, db: AsyncSession):
    if not is_admin(callback.from_user.id):
        await callback.answer("Нет доступа", show_alert=True)
        return
    
    from app.database.models import PromoCode
    
    result = await db.execute(
        select(PromoCode).order_by(PromoCode.created_at.desc()).limit(10)
    )
    promos = result.scalars().all()
    
    text = "🎁 <b>Промокоды</b>\n\n"
    
    if promos:
        for promo in promos:
            status = "✅" if promo.is_active else "❌"
            bonus = f"{promo.bonus_amount}₽" if promo.bonus_amount else f"{promo.bonus_days} дней"
            text += f"{status} <code>{promo.code}</code> - {bonus} ({promo.current_uses}/{promo.max_uses})\n"
    else:
        text += "Нет промокодов\n"
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="➕ Создать промокод", callback_data="admin_promo_create")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="back_admin")]
    ])
    
    await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="HTML")
    await callback.answer()


@router.callback_query(F.data == "admin_promo_create")
async def callback_admin_promo_create(callback: CallbackQuery, state: FSMContext):
    if not is_admin(callback.from_user.id):
        await callback.answer("Нет доступа", show_alert=True)
        return
    
    await callback.message.edit_text(
        "Введите код промокода (или 'auto' для автогенерации):",
        reply_markup=get_back_keyboard(),
        parse_mode="HTML"
    )
    await state.set_state(AdminStates.waiting_promo_code)
    await callback.answer()


@router.message(AdminStates.waiting_promo_code)
async def process_promo_code(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return
    
    import random
    import string
    
    code = message.text.strip().upper()
    if code == "AUTO":
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    
    await state.update_data(promo_code=code)
    await state.set_state(AdminStates.waiting_promo_discount)
    
    await message.answer(f"Код: <code>{code}</code>\n\nВведите сумму скидки в рублях:", parse_mode="HTML")


@router.message(AdminStates.waiting_promo_discount)
async def process_promo_discount(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return
    
    try:
        discount = float(message.text.replace(",", "."))
    except ValueError:
        await message.answer("Введите корректную сумму")
        return
    
    await state.update_data(promo_discount=discount)
    await state.set_state(AdminStates.waiting_promo_uses)
    
    await message.answer("Введите максимальное количество использований:")


@router.message(AdminStates.waiting_promo_uses)
async def process_promo_uses(message: Message, db: AsyncSession, state: FSMContext):
    if not is_admin(message.from_user.id):
        return
    
    try:
        max_uses = int(message.text)
    except ValueError:
        await message.answer("Введите целое число")
        return
    
    data = await state.get_data()
    code = data.get("promo_code")
    bonus_amount = data.get("promo_discount")
    
    await state.clear()
    
    from app.database.models import PromoCode
    from datetime import datetime
    
    promo = PromoCode(
        code=code,
        bonus_amount=bonus_amount,
        max_uses=max_uses,
        current_uses=0,
        is_active=True,
        created_at=datetime.utcnow()
    )
    db.add(promo)
    await db.commit()
    
    await message.answer(
        f"✅ Промокод создан!\n\n"
        f"🎁 Код: <code>{code}</code>\n"
        f"💰 Бонус: {bonus_amount}₽\n"
        f"🔢 Использований: {max_uses}",
        reply_markup=get_admin_keyboard(),
        parse_mode="HTML"
    )


@router.callback_query(F.data == "admin_settings")
async def callback_admin_settings(callback: CallbackQuery, db: AsyncSession):
    if not is_admin(callback.from_user.id):
        await callback.answer("Нет доступа", show_alert=True)
        return
    
    text = f"""
⚙️ <b>Настройки бота</b>

💰 Цена за день: <b>{settings.SUBSCRIPTION_DAILY_PRICE}₽</b>
🎁 Пробный период: <b>{settings.TRIAL_DAYS} дней</b>
"""
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="back_admin")]
    ])
    
    await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="HTML")
    await callback.answer()


@router.callback_query(F.data == "back_admin")
async def callback_back_admin(callback: CallbackQuery, db: AsyncSession, state: FSMContext):
    if not is_admin(callback.from_user.id):
        await callback.answer("Нет доступа", show_alert=True)
        return
    
    await state.clear()
    
    result = await db.execute(select(func.count(User.id)))
    users_count = result.scalar()
    
    result = await db.execute(
        select(func.count(Subscription.id)).where(
            Subscription.status == SubscriptionStatus.ACTIVE
        )
    )
    active_count = result.scalar()
    
    result = await db.execute(select(func.sum(User.balance)))
    total_balance = result.scalar() or 0.0
    
    text = get_text(
        "admin_panel",
        users_count=users_count,
        active_count=active_count,
        total_balance=total_balance
    )
    
    await callback.message.edit_text(text, reply_markup=get_admin_keyboard(), parse_mode="HTML")
    await callback.answer()
