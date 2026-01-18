from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from typing import Optional
from app.config import settings


def get_main_menu_keyboard(webapp_url: Optional[str] = None, user_id: Optional[int] = None) -> InlineKeyboardMarkup:
    buttons = []
    
    if webapp_url:
        buttons.append([
            InlineKeyboardButton(text="📱 ПОДКЛЮЧИТЬСЯ", web_app=WebAppInfo(url=webapp_url))
        ])
    
    buttons.append([
        InlineKeyboardButton(text="❓ Не открывается?", callback_data="not_opening_menu")
    ])
    
    if user_id and settings.is_admin(user_id):
        buttons.append([
            InlineKeyboardButton(text="🛠 Админ панель", callback_data="admin_panel")
        ])
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_not_opening_menu_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(text="💰 Пополнить баланс", callback_data="deposit"),
            InlineKeyboardButton(text="📊 Мой профиль", callback_data="profile")
        ],
        [
            InlineKeyboardButton(text="🔐 VPN подписка", callback_data="subscription"),
            InlineKeyboardButton(text="❓ Помощь", callback_data="help")
        ],
        [
            InlineKeyboardButton(text="◀️ Назад", callback_data="back_to_main")
        ]
    ]
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


def get_happ_download_button_row(
    platform: str = "android"
) -> list:
    """Get download button row for HApp."""
    if platform == "android":
        return [InlineKeyboardButton(text="📱 Скачать приложение (Android)", url="https://play.google.com/store")]
    elif platform == "ios":
        return [InlineKeyboardButton(text="📱 Скачать приложение (iOS)", url="https://apps.apple.com/")]
    return []


def get_offer_keyboard(offer_id: int) -> InlineKeyboardMarkup:
    """Get keyboard for promo offer."""
    buttons = [
        [InlineKeyboardButton(text="✅ Принять предложение", callback_data=f"accept_offer_{offer_id}")],
        [InlineKeyboardButton(text="❌ Отклонить", callback_data=f"decline_offer_{offer_id}")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_admin_tickets_keyboard(
    tickets: list,
    page: int = 1,
    total_pages: int = 1
) -> InlineKeyboardMarkup:
    """Get keyboard for admin ticket list."""
    buttons = []
    for ticket in tickets:
        ticket_id = ticket.id if hasattr(ticket, 'id') else ticket.get('id', 0)
        status = ticket.status if hasattr(ticket, 'status') else ticket.get('status', '')
        buttons.append([InlineKeyboardButton(
            text=f"🎫 #{ticket_id} - {status}",
            callback_data=f"admin_view_ticket_{ticket_id}"
        )])
    
    if total_pages > 1:
        nav_row = []
        if page > 1:
            nav_row.append(InlineKeyboardButton(text="◀️", callback_data=f"admin_tickets_page_{page-1}"))
        nav_row.append(InlineKeyboardButton(text=f"{page}/{total_pages}", callback_data="noop"))
        if page < total_pages:
            nav_row.append(InlineKeyboardButton(text="▶️", callback_data=f"admin_tickets_page_{page+1}"))
        buttons.append(nav_row)
    
    buttons.append([InlineKeyboardButton(text="⬅️ Назад", callback_data="admin_panel")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_admin_ticket_view_keyboard(ticket_id: int) -> InlineKeyboardMarkup:
    """Get keyboard for viewing a single ticket."""
    buttons = [
        [InlineKeyboardButton(text="💬 Ответить", callback_data=f"admin_reply_ticket_{ticket_id}")],
        [InlineKeyboardButton(text="✅ Закрыть", callback_data=f"admin_close_ticket_{ticket_id}")],
        [InlineKeyboardButton(text="⬅️ К списку", callback_data="admin_tickets")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_admin_ticket_reply_cancel_keyboard(ticket_id: int) -> InlineKeyboardMarkup:
    """Get keyboard for canceling ticket reply."""
    buttons = [
        [InlineKeyboardButton(text="❌ Отмена", callback_data=f"admin_view_ticket_{ticket_id}")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
