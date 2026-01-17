from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from typing import Optional


def get_main_menu_keyboard(webapp_url: Optional[str] = None) -> InlineKeyboardMarkup:
    buttons = []
    
    if webapp_url:
        buttons.append([
            InlineKeyboardButton(text="📱 Открыть приложение", web_app=WebAppInfo(url=webapp_url))
        ])
    
    buttons.extend([
        [
            InlineKeyboardButton(text="💰 Пополнить баланс", callback_data="deposit"),
            InlineKeyboardButton(text="📊 Мой профиль", callback_data="profile")
        ],
        [
            InlineKeyboardButton(text="🔐 VPN подписка", callback_data="subscription"),
            InlineKeyboardButton(text="❓ Помощь", callback_data="help")
        ]
    ])
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_deposit_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(text="60₽ (10 дней)", callback_data="deposit_60"),
            InlineKeyboardButton(text="180₽ (30 дней)", callback_data="deposit_180")
        ],
        [
            InlineKeyboardButton(text="360₽ (60 дней)", callback_data="deposit_360"),
            InlineKeyboardButton(text="540₽ (90 дней)", callback_data="deposit_540")
        ],
        [
            InlineKeyboardButton(text="💳 Другая сумма", callback_data="deposit_custom")
        ],
        [
            InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_menu")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_payment_keyboard(payment_url: str) -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="💳 Оплатить", url=payment_url)],
        [InlineKeyboardButton(text="✅ Я оплатил", callback_data="check_payment")],
        [InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_payment")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_subscription_keyboard(has_subscription: bool = False) -> InlineKeyboardMarkup:
    buttons = []
    
    if has_subscription:
        buttons.append([
            InlineKeyboardButton(text="📋 Получить ключ", callback_data="get_key")
        ])
        buttons.append([
            InlineKeyboardButton(text="🔄 Обновить ключ", callback_data="refresh_key")
        ])
    else:
        buttons.append([
            InlineKeyboardButton(text="🆓 Активировать пробный период", callback_data="activate_trial")
        ])
        buttons.append([
            InlineKeyboardButton(text="💰 Пополнить и активировать", callback_data="deposit")
        ])
    
    buttons.append([
        InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_menu")
    ])
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_back_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_menu")]
    ])


def get_channel_sub_keyboard(channel_url: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📢 Подписаться на канал", url=channel_url)],
        [InlineKeyboardButton(text="✅ Проверить подписку", callback_data="check_channel")]
    ])


def get_admin_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(text="📊 Статистика", callback_data="admin_stats"),
            InlineKeyboardButton(text="👥 Пользователи", callback_data="admin_users")
        ],
        [
            InlineKeyboardButton(text="🔍 Поиск", callback_data="admin_search"),
            InlineKeyboardButton(text="💰 Баланс", callback_data="admin_add_balance")
        ],
        [
            InlineKeyboardButton(text="📢 Рассылка", callback_data="admin_broadcast"),
            InlineKeyboardButton(text="🎁 Промокоды", callback_data="admin_promo")
        ],
        [
            InlineKeyboardButton(text="⚙️ Настройки", callback_data="admin_settings")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
