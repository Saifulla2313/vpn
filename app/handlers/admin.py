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
from app.localization.texts import get_text
from app.config import settings

logger = logging.getLogger(__name__)
router = Router()


class AdminStates(StatesGroup):
    waiting_user_id = State()
    waiting_balance_amount = State()
    waiting_broadcast = State()


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
