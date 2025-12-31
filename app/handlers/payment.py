import logging
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.crud.user import get_user_by_telegram_id, update_user_balance
from app.database.crud.subscription import get_subscription_by_user_id, activate_subscription
from app.database.crud.transaction import create_transaction, get_transaction_by_payment_id, complete_transaction
from app.database.models import TransactionType, TransactionStatus, SubscriptionStatus
from app.keyboards.inline import get_deposit_keyboard, get_payment_keyboard, get_back_keyboard
from app.localization.texts import get_text
from app.config import settings
from app.services.yookassa_service import YooKassaService

logger = logging.getLogger(__name__)
router = Router()


class PaymentStates(StatesGroup):
    waiting_amount = State()
    waiting_payment = State()


@router.callback_query(F.data == "deposit")
async def callback_deposit(callback: CallbackQuery, db: AsyncSession):
    user = await get_user_by_telegram_id(db, callback.from_user.id)
    if not user:
        await callback.answer("Ошибка: пользователь не найден", show_alert=True)
        return
    
    text = get_text("deposit_menu", balance=user.balance)
    await callback.message.edit_text(
        text,
        reply_markup=get_deposit_keyboard(),
        parse_mode="HTML"
    )
    await callback.answer()


async def create_yookassa_payment(
    db: AsyncSession,
    user,
    amount: float,
    callback: CallbackQuery
) -> bool:
    yookassa = YooKassaService()
    
    if not yookassa.configured:
        await callback.answer("Платежная система временно недоступна", show_alert=True)
        return False
    
    transaction = await create_transaction(
        db,
        user_id=user.id,
        transaction_type=TransactionType.DEPOSIT,
        amount=amount,
        description=f"Пополнение баланса на {amount}₽",
        payment_method="yookassa"
    )
    
    metadata = {
        "user_id": str(user.id),
        "telegram_id": str(user.telegram_id),
        "transaction_id": str(transaction.id)
    }
    
    payment_result = await yookassa.create_payment(
        amount=amount,
        currency="RUB",
        description=f"Пополнение баланса VPN бота",
        metadata=metadata
    )
    
    if not payment_result or payment_result.get("error"):
        await callback.answer("Ошибка создания платежа", show_alert=True)
        return False
    
    transaction.payment_id = payment_result["id"]
    await db.commit()
    
    payment_url = payment_result["confirmation_url"]
    
    text = get_text("payment_created", amount=amount)
    await callback.message.edit_text(
        text,
        reply_markup=get_payment_keyboard(payment_url),
        parse_mode="HTML"
    )
    
    return True


@router.callback_query(F.data.startswith("deposit_"))
async def callback_deposit_amount(callback: CallbackQuery, db: AsyncSession, state: FSMContext):
    user = await get_user_by_telegram_id(db, callback.from_user.id)
    if not user:
        await callback.answer("Ошибка: пользователь не найден", show_alert=True)
        return
    
    amount_str = callback.data.replace("deposit_", "")
    
    if amount_str == "custom":
        await callback.message.edit_text(
            "💰 Введите сумму пополнения (минимум 60₽):",
            reply_markup=get_back_keyboard(),
            parse_mode="HTML"
        )
        await state.set_state(PaymentStates.waiting_amount)
        await callback.answer()
        return
    
    try:
        amount = float(amount_str)
    except ValueError:
        await callback.answer("Неверная сумма", show_alert=True)
        return
    
    await create_yookassa_payment(db, user, amount, callback)
    await callback.answer()


@router.message(PaymentStates.waiting_amount)
async def process_custom_amount(message: Message, db: AsyncSession, state: FSMContext):
    try:
        amount = float(message.text.replace(",", "."))
        if amount < 60:
            await message.answer("Минимальная сумма пополнения - 60₽")
            return
        if amount > 100000:
            await message.answer("Максимальная сумма - 100 000₽")
            return
    except ValueError:
        await message.answer("Пожалуйста, введите корректную сумму")
        return
    
    user = await get_user_by_telegram_id(db, message.from_user.id)
    if not user:
        await message.answer("Ошибка: пользователь не найден")
        return
    
    await state.clear()
    
    yookassa = YooKassaService()
    
    if not yookassa.configured:
        await message.answer("Платежная система временно недоступна")
        return
    
    transaction = await create_transaction(
        db,
        user_id=user.id,
        transaction_type=TransactionType.DEPOSIT,
        amount=amount,
        description=f"Пополнение баланса на {amount}₽",
        payment_method="yookassa"
    )
    
    metadata = {
        "user_id": str(user.id),
        "telegram_id": str(user.telegram_id),
        "transaction_id": str(transaction.id)
    }
    
    payment_result = await yookassa.create_payment(
        amount=amount,
        currency="RUB",
        description=f"Пополнение баланса VPN бота",
        metadata=metadata
    )
    
    if not payment_result or payment_result.get("error"):
        await message.answer("Ошибка создания платежа. Попробуйте позже.")
        return
    
    transaction.payment_id = payment_result["id"]
    await db.commit()
    
    payment_url = payment_result["confirmation_url"]
    text = get_text("payment_created", amount=amount)
    
    await message.answer(
        text,
        reply_markup=get_payment_keyboard(payment_url),
        parse_mode="HTML"
    )


@router.callback_query(F.data == "check_payment")
async def callback_check_payment(callback: CallbackQuery, db: AsyncSession):
    user = await get_user_by_telegram_id(db, callback.from_user.id)
    if not user:
        await callback.answer("Ошибка: пользователь не найден", show_alert=True)
        return
    
    from app.database.crud.transaction import get_user_transactions
    transactions = await get_user_transactions(db, user.id, limit=1)
    
    if not transactions:
        await callback.answer("Платеж не найден", show_alert=True)
        return
    
    transaction = transactions[0]
    
    if transaction.status == TransactionStatus.COMPLETED:
        await callback.answer("Платеж уже обработан", show_alert=True)
        return
    
    if not transaction.payment_id:
        await callback.answer("Платеж не найден", show_alert=True)
        return
    
    yookassa = YooKassaService()
    payment_info = await yookassa.get_payment_info(transaction.payment_id)
    
    if not payment_info:
        await callback.answer("Не удалось проверить платеж", show_alert=True)
        return
    
    if payment_info["status"] == "succeeded" and payment_info["paid"]:
        await complete_transaction(db, transaction.id)
        await update_user_balance(db, user.id, transaction.amount)
        
        await db.refresh(user)
        
        subscription = await get_subscription_by_user_id(db, user.id)
        subscription_info = ""
        
        if subscription and subscription.status != SubscriptionStatus.ACTIVE:
            if user.balance >= settings.SUBSCRIPTION_DAILY_PRICE:
                days = int(user.balance // settings.SUBSCRIPTION_DAILY_PRICE)
                await activate_subscription(db, user.id, days)
                subscription_info = f"✅ Подписка активирована на {days} дней!"
        elif subscription and subscription.status == SubscriptionStatus.ACTIVE:
            subscription_info = "✅ Подписка продлена автоматически"
        
        text = get_text(
            "payment_success",
            amount=transaction.amount,
            balance=user.balance,
            subscription_info=subscription_info
        )
        
        await callback.message.edit_text(
            text,
            reply_markup=get_back_keyboard(),
            parse_mode="HTML"
        )
        await callback.answer("Оплата успешна!")
        
    elif payment_info["status"] == "pending":
        await callback.answer("Платеж еще обрабатывается. Подождите.", show_alert=True)
    else:
        await callback.answer("Платеж не был оплачен", show_alert=True)


@router.callback_query(F.data == "cancel_payment")
async def callback_cancel_payment(callback: CallbackQuery):
    from app.handlers.start import get_webapp_url
    from app.keyboards.inline import get_main_menu_keyboard
    
    await callback.message.edit_text(
        get_text("welcome"),
        reply_markup=get_main_menu_keyboard(get_webapp_url()),
        parse_mode="HTML"
    )
    await callback.answer("Платеж отменен")
