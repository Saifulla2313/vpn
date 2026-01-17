from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from typing import Optional


def get_admin_main_keyboard(language: str = "ru") -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(text="👥 Пользователи", callback_data="admin_submenu_users"),
            InlineKeyboardButton(text="💰 Промо и статистика", callback_data="admin_submenu_promo")
        ],
        [
            InlineKeyboardButton(text="📨 Коммуникации", callback_data="admin_submenu_communications"),
            InlineKeyboardButton(text="🎫 Поддержка", callback_data="admin_submenu_support")
        ],
        [
            InlineKeyboardButton(text="⚙️ Настройки", callback_data="admin_submenu_settings"),
            InlineKeyboardButton(text="🔧 Система", callback_data="admin_submenu_system")
        ],
        [
            InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_menu")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_admin_users_submenu_keyboard(language: str = "ru") -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(text="🔍 Поиск пользователя", callback_data="admin_search_user"),
            InlineKeyboardButton(text="👥 Список пользователей", callback_data="admin_users_list")
        ],
        [
            InlineKeyboardButton(text="📊 Подписки", callback_data="admin_subscriptions"),
            InlineKeyboardButton(text="🎁 Триалы", callback_data="admin_trials")
        ],
        [
            InlineKeyboardButton(text="🚫 Черный список", callback_data="admin_blacklist"),
            InlineKeyboardButton(text="🔨 Массовый бан", callback_data="admin_bulk_ban")
        ],
        [
            InlineKeyboardButton(text="⬅️ Назад", callback_data="admin_panel")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_admin_promo_submenu_keyboard(language: str = "ru") -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(text="🎁 Промокоды", callback_data="admin_promocodes"),
            InlineKeyboardButton(text="📊 Статистика", callback_data="admin_statistics")
        ],
        [
            InlineKeyboardButton(text="🎯 Промо группы", callback_data="admin_promo_groups"),
            InlineKeyboardButton(text="💎 Промо офферы", callback_data="admin_promo_offers")
        ],
        [
            InlineKeyboardButton(text="👥 Рефералы", callback_data="admin_referrals"),
            InlineKeyboardButton(text="💳 Платежи", callback_data="admin_payments")
        ],
        [
            InlineKeyboardButton(text="⬅️ Назад", callback_data="admin_panel")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_admin_communications_submenu_keyboard(language: str = "ru") -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(text="📢 Рассылка", callback_data="admin_broadcast"),
            InlineKeyboardButton(text="📝 Сообщения", callback_data="admin_messages")
        ],
        [
            InlineKeyboardButton(text="👋 Приветствие", callback_data="admin_welcome_text"),
            InlineKeyboardButton(text="📋 Опросы", callback_data="admin_polls")
        ],
        [
            InlineKeyboardButton(text="🎉 Конкурсы", callback_data="admin_contests"),
            InlineKeyboardButton(text="📅 Ежедневные", callback_data="admin_daily_contests")
        ],
        [
            InlineKeyboardButton(text="🎯 Кампании", callback_data="admin_campaigns")
        ],
        [
            InlineKeyboardButton(text="⬅️ Назад", callback_data="admin_panel")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_admin_support_submenu_keyboard(language: str = "ru") -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(text="🎫 Тикеты", callback_data="admin_tickets"),
            InlineKeyboardButton(text="❓ FAQ", callback_data="admin_faq")
        ],
        [
            InlineKeyboardButton(text="📜 Правила", callback_data="admin_rules"),
            InlineKeyboardButton(text="⚙️ Настройки поддержки", callback_data="admin_support_settings")
        ],
        [
            InlineKeyboardButton(text="📋 Аудит поддержки", callback_data="admin_support_audit")
        ],
        [
            InlineKeyboardButton(text="⬅️ Назад", callback_data="admin_panel")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_admin_settings_submenu_keyboard(language: str = "ru") -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(text="🤖 Конфигурация бота", callback_data="admin_bot_config"),
            InlineKeyboardButton(text="💰 Тарифы", callback_data="admin_tariffs")
        ],
        [
            InlineKeyboardButton(text="🖥️ Серверы", callback_data="admin_servers"),
            InlineKeyboardButton(text="🌐 RemnaWave", callback_data="admin_remnawave")
        ],
        [
            InlineKeyboardButton(text="📄 Публичная оферта", callback_data="admin_public_offer"),
            InlineKeyboardButton(text="🔒 Политика", callback_data="admin_privacy_policy")
        ],
        [
            InlineKeyboardButton(text="⬅️ Назад", callback_data="admin_panel")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_admin_system_submenu_keyboard(language: str = "ru") -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(text="📊 Мониторинг", callback_data="admin_monitoring"),
            InlineKeyboardButton(text="💾 Бэкапы", callback_data="admin_backups")
        ],
        [
            InlineKeyboardButton(text="🔧 Обслуживание", callback_data="admin_maintenance"),
            InlineKeyboardButton(text="📝 Логи", callback_data="admin_system_logs")
        ],
        [
            InlineKeyboardButton(text="🔄 Обновления", callback_data="admin_updates"),
            InlineKeyboardButton(text="📊 Отчёты", callback_data="admin_reports")
        ],
        [
            InlineKeyboardButton(text="⬅️ Назад", callback_data="admin_panel")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_admin_back_keyboard(language: str = "ru") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="admin_panel")]
    ])
