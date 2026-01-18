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


def get_admin_users_keyboard(language: str = "ru") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🔍 Поиск", callback_data="admin_users_search"),
            InlineKeyboardButton(text="👥 Список", callback_data="admin_users_list")
        ],
        [
            InlineKeyboardButton(text="📊 Статистика", callback_data="admin_users_stats"),
            InlineKeyboardButton(text="⚙️ Фильтры", callback_data="admin_users_filters")
        ],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="admin_submenu_users")]
    ])


def get_admin_subscriptions_keyboard(language: str = "ru") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="📋 Список", callback_data="admin_subs_list"),
            InlineKeyboardButton(text="⏰ Истекающие", callback_data="admin_subs_expiring")
        ],
        [
            InlineKeyboardButton(text="📊 Статистика", callback_data="admin_subs_stats"),
            InlineKeyboardButton(text="🌍 География", callback_data="admin_subs_countries")
        ],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="admin_submenu_users")]
    ])


def get_admin_trials_keyboard(language: str = "ru") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="♻️ Сбросить триалы", callback_data="admin_trials_reset")],
        [InlineKeyboardButton(text="🔄 Обновить", callback_data="admin_trials")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="admin_submenu_users")]
    ])


def get_admin_promocodes_keyboard(language: str = "ru") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="📋 Список", callback_data="admin_promo_list"),
            InlineKeyboardButton(text="➕ Создать", callback_data="admin_promo_create")
        ],
        [
            InlineKeyboardButton(text="📊 Статистика", callback_data="admin_promo_stats")
        ],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="admin_submenu_promo")]
    ])


def get_admin_statistics_keyboard(language: str = "ru") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="👥 Пользователи", callback_data="admin_stats_users"),
            InlineKeyboardButton(text="📱 Подписки", callback_data="admin_stats_subs")
        ],
        [
            InlineKeyboardButton(text="💰 Доходы", callback_data="admin_stats_revenue"),
            InlineKeyboardButton(text="🤝 Рефералы", callback_data="admin_stats_referrals")
        ],
        [InlineKeyboardButton(text="📊 Общая сводка", callback_data="admin_stats_summary")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="admin_submenu_promo")]
    ])


def get_admin_tickets_keyboard(
    tickets: list,
    current_page: int = 1,
    total_pages: int = 1,
    language: str = "ru",
    scope: str = "open",
    back_callback: str = "admin_submenu_support"
) -> InlineKeyboardMarkup:
    keyboard = []
    scope_row = [
        InlineKeyboardButton(
            text="📬 Открытые" if scope != "open" else "📬 Открытые ✓",
            callback_data="admin_tickets_scope_open"
        ),
        InlineKeyboardButton(
            text="📪 Закрытые" if scope != "closed" else "📪 Закрытые ✓",
            callback_data="admin_tickets_scope_closed"
        )
    ]
    keyboard.append(scope_row)
    for ticket in tickets:
        text = f"{ticket['status_emoji']} {ticket['priority_emoji']} #{ticket['id']} {ticket['locked_emoji']} {ticket['user_name'][:20]}"
        keyboard.append([
            InlineKeyboardButton(text=text, callback_data=f"admin_view_ticket_{ticket['id']}")
        ])
    if total_pages > 1:
        nav_row = []
        if current_page > 1:
            nav_row.append(InlineKeyboardButton(text="⬅️", callback_data=f"admin_tickets_page_{scope}_{current_page - 1}"))
        nav_row.append(InlineKeyboardButton(text=f"{current_page}/{total_pages}", callback_data="noop"))
        if current_page < total_pages:
            nav_row.append(InlineKeyboardButton(text="➡️", callback_data=f"admin_tickets_page_{scope}_{current_page + 1}"))
        keyboard.append(nav_row)
    keyboard.append([InlineKeyboardButton(text="🔒 Закрыть все открытые", callback_data="admin_tickets_close_all")])
    keyboard.append([InlineKeyboardButton(text="⬅️ Назад", callback_data=back_callback)])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_admin_ticket_view_keyboard(
    ticket_id: int,
    is_closed: bool = False,
    language: str = "ru",
    is_user_blocked: bool = False
) -> InlineKeyboardMarkup:
    keyboard = []
    if not is_closed:
        keyboard.append([InlineKeyboardButton(text="💬 Ответить", callback_data=f"admin_reply_ticket_{ticket_id}")])
        keyboard.append([InlineKeyboardButton(text="✅ Закрыть тикет", callback_data=f"admin_close_ticket_{ticket_id}")])
    else:
        keyboard.append([InlineKeyboardButton(text="🔓 Переоткрыть", callback_data=f"admin_reopen_ticket_{ticket_id}")])
    if is_user_blocked:
        keyboard.append([InlineKeyboardButton(text="🔓 Разблокировать пользователя", callback_data=f"admin_ticket_unblock_{ticket_id}")])
    else:
        keyboard.append([InlineKeyboardButton(text="🔒 Заблокировать пользователя", callback_data=f"admin_ticket_block_{ticket_id}")])
    keyboard.append([InlineKeyboardButton(text="⬅️ К тикетам", callback_data="admin_tickets")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_admin_ticket_reply_cancel_keyboard(language: str = "ru") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="❌ Отмена", callback_data="admin_tickets")]
    ])


def get_admin_messages_keyboard(language: str = "ru") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="📢 Всем", callback_data="admin_msg_all"),
            InlineKeyboardButton(text="📋 По подпискам", callback_data="admin_msg_by_sub")
        ],
        [
            InlineKeyboardButton(text="⚙️ По критериям", callback_data="admin_msg_custom"),
            InlineKeyboardButton(text="📌 Закреп", callback_data="admin_pinned_message")
        ],
        [InlineKeyboardButton(text="📜 История", callback_data="admin_msg_history")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="admin_submenu_communications")]
    ])


def get_admin_campaigns_keyboard(language: str = "ru") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="📋 Список кампаний", callback_data="admin_campaigns_list"),
            InlineKeyboardButton(text="➕ Создать", callback_data="admin_campaigns_create")
        ],
        [InlineKeyboardButton(text="📊 Общая статистика", callback_data="admin_campaigns_stats")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="admin_submenu_communications")]
    ])


def get_admin_contests_keyboard(language: str = "ru") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="📋 Список конкурсов", callback_data="admin_contests_list"),
            InlineKeyboardButton(text="➕ Создать", callback_data="admin_contests_create")
        ],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="admin_contests")]
    ])


def get_admin_contests_root_keyboard(language: str = "ru") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎯 Реферальные конкурсы", callback_data="admin_referral_contests")],
        [InlineKeyboardButton(text="📅 Ежедневные конкурсы", callback_data="admin_daily_contests")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="admin_submenu_communications")]
    ])


def get_admin_reports_keyboard(language: str = "ru") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📊 Дневной отчет", callback_data="admin_reports_daily")],
        [InlineKeyboardButton(text="📈 Недельный отчет", callback_data="admin_reports_weekly")],
        [InlineKeyboardButton(text="📉 Месячный отчет", callback_data="admin_reports_monthly")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="admin_submenu_system")]
    ])


def get_admin_report_result_keyboard(language: str = "ru") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🗑️ Закрыть", callback_data="admin_close_report")],
        [InlineKeyboardButton(text="⬅️ К отчетам", callback_data="admin_reports")]
    ])


def get_admin_remnawave_keyboard(language: str = "ru") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🔄 Синхронизация", callback_data="admin_rw_sync"),
            InlineKeyboardButton(text="🌐 Серверы", callback_data="admin_rw_squads")
        ],
        [
            InlineKeyboardButton(text="📊 Статус панели", callback_data="admin_rw_status"),
            InlineKeyboardButton(text="🔗 Ноды", callback_data="admin_rw_nodes")
        ],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="admin_submenu_settings")]
    ])


def get_admin_pagination_keyboard(
    current_page: int,
    total_pages: int,
    callback_prefix: str,
    back_callback: str = "admin_panel",
    language: str = "ru"
) -> InlineKeyboardMarkup:
    keyboard = []
    nav_row = []
    if current_page > 1:
        nav_row.append(InlineKeyboardButton(text="⬅️", callback_data=f"{callback_prefix}_page_{current_page - 1}"))
    nav_row.append(InlineKeyboardButton(text=f"{current_page}/{total_pages}", callback_data="noop"))
    if current_page < total_pages:
        nav_row.append(InlineKeyboardButton(text="➡️", callback_data=f"{callback_prefix}_page_{current_page + 1}"))
    if nav_row:
        keyboard.append(nav_row)
    keyboard.append([InlineKeyboardButton(text="⬅️ Назад", callback_data=back_callback)])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_admin_users_filters_keyboard(language: str = "ru") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💰 По балансу", callback_data="admin_users_balance_list")],
        [InlineKeyboardButton(text="📶 По трафику", callback_data="admin_users_traffic_list")],
        [InlineKeyboardButton(text="🕒 По активности", callback_data="admin_users_activity_list")],
        [InlineKeyboardButton(text="💳 По тратам", callback_data="admin_users_spending_list")],
        [InlineKeyboardButton(text="🛒 По покупкам", callback_data="admin_users_purchases_list")],
        [InlineKeyboardButton(text="📢 По кампании", callback_data="admin_users_campaign_list")],
        [InlineKeyboardButton(text="♻️ Готовы к продлению", callback_data="admin_users_ready_to_renew_filter")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="admin_users")]
    ])


def get_maintenance_keyboard(
    language: str = "ru",
    is_active: bool = False,
    monitoring_active: bool = False,
    has_issues: bool = False
) -> InlineKeyboardMarkup:
    toggle_text = "❌ Выключить техработы" if is_active else "✅ Включить техработы"
    monitoring_text = "⏹️ Остановить мониторинг" if monitoring_active else "▶️ Запустить мониторинг"
    keyboard = [
        [InlineKeyboardButton(text=toggle_text, callback_data="maintenance_toggle")],
        [InlineKeyboardButton(text=monitoring_text, callback_data="maintenance_monitoring_toggle")],
        [InlineKeyboardButton(text="📊 Проверить панель", callback_data="maintenance_check_panel")],
        [InlineKeyboardButton(text="🔔 Уведомить пользователей", callback_data="maintenance_notify")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="admin_submenu_system")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_monitoring_keyboard(language: str = "ru") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📊 Статистика", callback_data="admin_mon_stats")],
        [InlineKeyboardButton(text="📋 Логи событий", callback_data="admin_mon_logs")],
        [InlineKeyboardButton(text="⚙️ Настройки", callback_data="admin_mon_settings")],
        [InlineKeyboardButton(text="🔄 Обновить", callback_data="admin_monitoring")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="admin_submenu_system")]
    ])


def get_monitoring_logs_keyboard(language: str = "ru") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔄 Обновить", callback_data="admin_mon_logs")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="admin_monitoring")]
    ])


def get_monitoring_logs_back_keyboard(language: str = "ru") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="admin_monitoring")]
    ])


def get_backup_main_keyboard(language: str = "ru") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🚀 Создать бекап", callback_data="backup_create"),
            InlineKeyboardButton(text="📥 Восстановить", callback_data="backup_restore")
        ],
        [
            InlineKeyboardButton(text="📋 Список бекапов", callback_data="backup_list"),
            InlineKeyboardButton(text="⚙️ Настройки", callback_data="backup_settings")
        ],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="admin_submenu_system")]
    ])


def get_backup_list_keyboard(backups: list, page: int = 1, per_page: int = 5) -> InlineKeyboardMarkup:
    from datetime import datetime
    keyboard = []
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    page_backups = backups[start_idx:end_idx]
    for backup in page_backups:
        try:
            if backup.get("timestamp"):
                dt = datetime.fromisoformat(backup["timestamp"].replace('Z', '+00:00'))
                date_str = dt.strftime("%d.%m %H:%M")
            else:
                date_str = "?"
        except:
            date_str = "?"
        size_str = f"{backup.get('file_size_mb', 0):.1f}MB"
        records_str = backup.get('total_records', '?')
        button_text = f"📦 {date_str} • {size_str} • {records_str} записей"
        keyboard.append([InlineKeyboardButton(text=button_text, callback_data=f"backup_manage_{backup['filename']}")])
    if len(backups) > per_page:
        total_pages = (len(backups) + per_page - 1) // per_page
        nav_row = []
        if page > 1:
            nav_row.append(InlineKeyboardButton(text="⬅️", callback_data=f"backup_list_page_{page-1}"))
        nav_row.append(InlineKeyboardButton(text=f"{page}/{total_pages}", callback_data="noop"))
        if page < total_pages:
            nav_row.append(InlineKeyboardButton(text="➡️", callback_data=f"backup_list_page_{page+1}"))
        keyboard.append(nav_row)
    keyboard.append([InlineKeyboardButton(text="⬅️ Назад", callback_data="backup_panel")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_backup_manage_keyboard(backup_filename: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📥 Восстановить", callback_data=f"backup_restore_file_{backup_filename}")],
        [InlineKeyboardButton(text="🗑️ Удалить", callback_data=f"backup_delete_{backup_filename}")],
        [InlineKeyboardButton(text="⬅️ К списку", callback_data="backup_list")]
    ])


def get_backup_settings_keyboard(settings_obj) -> InlineKeyboardMarkup:
    auto_status = "✅ Включены" if settings_obj.auto_backup_enabled else "❌ Отключены"
    compression_status = "✅ Включено" if settings_obj.compression_enabled else "❌ Отключено"
    logs_status = "✅ Включены" if settings_obj.include_logs else "❌ Отключены"
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"🔄 Автобекапы: {auto_status}", callback_data="backup_toggle_auto")],
        [InlineKeyboardButton(text=f"🗜️ Сжатие: {compression_status}", callback_data="backup_toggle_compression")],
        [InlineKeyboardButton(text=f"📋 Логи в бекапе: {logs_status}", callback_data="backup_toggle_logs")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="backup_panel")]
    ])


def get_support_settings_keyboard(language: str = "ru") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⚙️ Режим работы", callback_data="admin_support_mode")],
        [InlineKeyboardButton(text="📝 Описание", callback_data="admin_support_edit_desc")],
        [InlineKeyboardButton(text="🔔 Уведомления", callback_data="admin_support_notifications")],
        [InlineKeyboardButton(text="⏰ SLA", callback_data="admin_support_sla")],
        [InlineKeyboardButton(text="🧑‍⚖️ Модераторы", callback_data="admin_support_list_moderators")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="admin_submenu_support")]
    ])


def get_welcome_text_keyboard(language: str = "ru", is_enabled: bool = True) -> InlineKeyboardMarkup:
    toggle_text = "❌ Выключить" if is_enabled else "✅ Включить"
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📝 Текущий текст", callback_data="admin_welcome_view")],
        [InlineKeyboardButton(text="✏️ Редактировать", callback_data="admin_welcome_edit")],
        [InlineKeyboardButton(text=toggle_text, callback_data="admin_welcome_toggle")],
        [InlineKeyboardButton(text="❓ Плейсхолдеры", callback_data="admin_welcome_placeholders")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="admin_submenu_communications")]
    ])


def get_pinned_message_keyboard(
    language: str = "ru",
    send_before_menu: bool = True,
    send_on_every_start: bool = True
) -> InlineKeyboardMarkup:
    position_text = "⬆️ Перед меню" if send_before_menu else "⬇️ После меню"
    start_mode_text = "🔁 При каждом /start" if send_on_every_start else "🚫 Один раз"
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✏️ Обновить сообщение", callback_data="admin_pinned_update")],
        [InlineKeyboardButton(text=position_text, callback_data="admin_pinned_toggle_position")],
        [InlineKeyboardButton(text=start_mode_text, callback_data="admin_pinned_toggle_start_mode")],
        [InlineKeyboardButton(text="🗑️ Удалить", callback_data="admin_pinned_delete")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="admin_messages")]
    ])


def get_pinned_broadcast_confirm_keyboard(language: str = "ru", pinned_message_id: int = 0) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📢 Разослать сейчас", callback_data=f"admin_pinned_broadcast_now:{pinned_message_id}")],
        [InlineKeyboardButton(text="⏭️ Только при /start", callback_data=f"admin_pinned_broadcast_skip:{pinned_message_id}")],
        [InlineKeyboardButton(text="❌ Отмена", callback_data="admin_pinned_message")]
    ])


def get_broadcast_target_keyboard(language: str = "ru") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="👥 Всем активным", callback_data="broadcast_target_all")],
        [InlineKeyboardButton(text="💎 С подпиской", callback_data="broadcast_target_subscribed")],
        [InlineKeyboardButton(text="❌ Без подписки", callback_data="broadcast_target_no_sub")],
        [InlineKeyboardButton(text="🎁 С триалом", callback_data="broadcast_target_trial")],
        [InlineKeyboardButton(text="📦 По тарифу", callback_data="broadcast_target_tariff")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="admin_messages")]
    ])


def get_broadcast_media_keyboard(language: str = "ru") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📝 Только текст", callback_data="broadcast_media_text")],
        [InlineKeyboardButton(text="🖼️ С фото", callback_data="broadcast_media_photo")],
        [InlineKeyboardButton(text="🎬 С видео", callback_data="broadcast_media_video")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="admin_msg_all")]
    ])


def get_broadcast_history_keyboard(language: str = "ru", page: int = 1, total_pages: int = 1) -> InlineKeyboardMarkup:
    keyboard = []
    if total_pages > 1:
        nav_row = []
        if page > 1:
            nav_row.append(InlineKeyboardButton(text="⬅️", callback_data=f"admin_msg_history_page_{page - 1}"))
        nav_row.append(InlineKeyboardButton(text=f"{page}/{total_pages}", callback_data="noop"))
        if page < total_pages:
            nav_row.append(InlineKeyboardButton(text="➡️", callback_data=f"admin_msg_history_page_{page + 1}"))
        keyboard.append(nav_row)
    keyboard.append([InlineKeyboardButton(text="⬅️ Назад", callback_data="admin_messages")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_period_selection_keyboard(language: str = "ru") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Сегодня", callback_data="period_today"),
            InlineKeyboardButton(text="Вчера", callback_data="period_yesterday")
        ],
        [
            InlineKeyboardButton(text="Неделя", callback_data="period_week"),
            InlineKeyboardButton(text="Месяц", callback_data="period_month")
        ],
        [InlineKeyboardButton(text="Всё время", callback_data="period_all")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="admin_stats_revenue")]
    ])


def get_confirmation_keyboard(action: str, item_id: int, language: str = "ru") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Да", callback_data=f"{action}_confirm_{item_id}"),
            InlineKeyboardButton(text="❌ Нет", callback_data=f"{action}_cancel_{item_id}")
        ]
    ])


def get_logs_keyboard(language: str = "ru") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔄 Обновить", callback_data="admin_system_logs_refresh")],
        [InlineKeyboardButton(text="⬇️ Скачать лог", callback_data="admin_system_logs_download")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="admin_submenu_system")]
    ])


def get_updates_keyboard(language: str = "ru") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔄 Проверить обновления", callback_data="admin_updates_check")],
        [InlineKeyboardButton(text="📋 Информация о версии", callback_data="admin_updates_info")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="admin_submenu_system")]
    ])


def get_version_info_keyboard(language: str = "ru") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔄 Обновить", callback_data="admin_updates_info")],
        [InlineKeyboardButton(text="⬅️ К обновлениям", callback_data="admin_updates")]
    ])


def get_tariffs_list_keyboard(tariffs: list, language: str = "ru", page: int = 0, total_pages: int = 1) -> InlineKeyboardMarkup:
    buttons = []
    for tariff_data in tariffs:
        if isinstance(tariff_data, tuple):
            tariff, subs_count = tariff_data
        else:
            tariff = tariff_data
            subs_count = 0
        status = "✅" if tariff.is_active else "❌"
        button_text = f"{status} {tariff.name} ({subs_count})"
        buttons.append([InlineKeyboardButton(text=button_text, callback_data=f"admin_tariff_view:{tariff.id}")])
    nav_buttons = []
    if page > 0:
        nav_buttons.append(InlineKeyboardButton(text="◀️", callback_data=f"admin_tariffs_page:{page-1}"))
    if page < total_pages - 1:
        nav_buttons.append(InlineKeyboardButton(text="▶️", callback_data=f"admin_tariffs_page:{page+1}"))
    if nav_buttons:
        buttons.append(nav_buttons)
    buttons.append([InlineKeyboardButton(text="➕ Создать тариф", callback_data="admin_tariff_create")])
    buttons.append([InlineKeyboardButton(text="⬅️ Назад", callback_data="admin_submenu_settings")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_tariff_view_keyboard(tariff_id: int, language: str = "ru") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✏️ Название", callback_data=f"admin_tariff_edit_name:{tariff_id}"),
            InlineKeyboardButton(text="📝 Описание", callback_data=f"admin_tariff_edit_desc:{tariff_id}")
        ],
        [
            InlineKeyboardButton(text="📊 Трафик", callback_data=f"admin_tariff_edit_traffic:{tariff_id}"),
            InlineKeyboardButton(text="📱 Устройства", callback_data=f"admin_tariff_edit_devices:{tariff_id}")
        ],
        [
            InlineKeyboardButton(text="💰 Цены", callback_data=f"admin_tariff_edit_prices:{tariff_id}"),
            InlineKeyboardButton(text="🎚️ Уровень", callback_data=f"admin_tariff_edit_tier:{tariff_id}")
        ],
        [
            InlineKeyboardButton(text="✅/❌ Статус", callback_data=f"admin_tariff_toggle:{tariff_id}"),
            InlineKeyboardButton(text="🗑️ Удалить", callback_data=f"admin_tariff_delete:{tariff_id}")
        ],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="admin_tariffs")]
    ])


def get_user_management_keyboard(user_id: int, language: str = "ru") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="💰 Баланс", callback_data=f"admin_user_balance_{user_id}"),
            InlineKeyboardButton(text="📱 Подписка", callback_data=f"admin_user_subscription_{user_id}")
        ],
        [
            InlineKeyboardButton(text="✉️ Написать", callback_data=f"admin_user_message_{user_id}"),
            InlineKeyboardButton(text="📊 Транзакции", callback_data=f"admin_user_transactions_{user_id}")
        ],
        [
            InlineKeyboardButton(text="🏷️ Промогруппа", callback_data=f"admin_user_promo_group_{user_id}"),
            InlineKeyboardButton(text="⚠️ Ограничения", callback_data=f"admin_user_restrictions_{user_id}")
        ],
        [
            InlineKeyboardButton(text="🚫 Заблокировать", callback_data=f"admin_user_block_{user_id}"),
            InlineKeyboardButton(text="🔓 Разблокировать", callback_data=f"admin_user_unblock_{user_id}")
        ],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="admin_users")]
    ])


def get_user_messages_keyboard(user_id: int, language: str = "ru") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✉️ Отправить сообщение", callback_data=f"admin_user_send_msg_{user_id}")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data=f"admin_user_manage_{user_id}")]
    ])


def get_user_restrictions_keyboard(user_id: int, language: str = "ru") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🚫 Заблокировать", callback_data=f"admin_user_block_{user_id}")],
        [InlineKeyboardButton(text="🔓 Разблокировать", callback_data=f"admin_user_unblock_{user_id}")],
        [InlineKeyboardButton(text="♻️ Сбросить триал", callback_data=f"admin_user_reset_trial_{user_id}")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data=f"admin_user_manage_{user_id}")]
    ])


def get_user_promo_group_keyboard(user_id: int, language: str = "ru") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🏷️ Изменить группу", callback_data=f"admin_user_change_promo_group_{user_id}")],
        [InlineKeyboardButton(text="❌ Убрать из группы", callback_data=f"admin_user_remove_promo_group_{user_id}")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data=f"admin_user_manage_{user_id}")]
    ])


def get_squad_management_keyboard(language: str = "ru") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📋 Список серверов", callback_data="admin_rw_squads_list")],
        [InlineKeyboardButton(text="➕ Создать сервер", callback_data="admin_rw_squad_create")],
        [InlineKeyboardButton(text="🔄 Синхронизировать", callback_data="admin_rw_squads_sync")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="admin_remnawave")]
    ])


def get_squad_edit_keyboard(squad_id: int, language: str = "ru") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✏️ Переименовать", callback_data=f"admin_rw_squad_rename_{squad_id}")],
        [InlineKeyboardButton(text="🌐 Inbounds", callback_data=f"admin_rw_squad_inbounds_{squad_id}")],
        [InlineKeyboardButton(text="✅/❌ Статус", callback_data=f"admin_rw_squad_toggle_{squad_id}")],
        [InlineKeyboardButton(text="🔄 Миграция", callback_data=f"admin_rw_squad_migrate_{squad_id}")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="admin_rw_squads")]
    ])


def get_node_management_keyboard(language: str = "ru") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📋 Список нод", callback_data="admin_rw_nodes_list")],
        [InlineKeyboardButton(text="🔄 Обновить статус", callback_data="admin_rw_nodes_refresh")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="admin_remnawave")]
    ])


def get_sync_options_keyboard(language: str = "ru") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔄 Полная синхронизация", callback_data="admin_rw_sync_full")],
        [InlineKeyboardButton(text="👥 Только пользователи", callback_data="admin_rw_sync_users")],
        [InlineKeyboardButton(text="🌐 Только серверы", callback_data="admin_rw_sync_servers")],
        [InlineKeyboardButton(text="⏰ Автосинхронизация", callback_data="admin_rw_auto_sync")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="admin_remnawave")]
    ])


def get_campaign_management_keyboard(campaign_id: int, is_active: bool = True, language: str = "ru") -> InlineKeyboardMarkup:
    toggle_text = "⏸️ Отключить" if is_active else "▶️ Включить"
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✏️ Редактировать", callback_data=f"admin_campaign_edit_{campaign_id}")],
        [InlineKeyboardButton(text=toggle_text, callback_data=f"admin_campaign_toggle_{campaign_id}")],
        [InlineKeyboardButton(text="📊 Статистика", callback_data=f"admin_campaign_stats_{campaign_id}")],
        [InlineKeyboardButton(text="🔗 Скопировать ссылку", callback_data=f"admin_campaign_link_{campaign_id}")],
        [InlineKeyboardButton(text="🗑️ Удалить", callback_data=f"admin_campaign_delete_{campaign_id}")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="admin_campaigns")]
    ])


def get_campaign_edit_keyboard(campaign_id: int, is_balance_bonus: bool = True, language: str = "ru") -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton(text="✏️ Название", callback_data=f"admin_campaign_edit_name_{campaign_id}")],
        [InlineKeyboardButton(text="🔗 Стартовый параметр", callback_data=f"admin_campaign_edit_start_{campaign_id}")]
    ]
    if is_balance_bonus:
        keyboard.append([InlineKeyboardButton(text="💰 Бонус на баланс", callback_data=f"admin_campaign_edit_balance_{campaign_id}")])
    else:
        keyboard.append([InlineKeyboardButton(text="📅 Дни подписки", callback_data=f"admin_campaign_edit_days_{campaign_id}")])
        keyboard.append([InlineKeyboardButton(text="📶 Трафик", callback_data=f"admin_campaign_edit_traffic_{campaign_id}")])
        keyboard.append([InlineKeyboardButton(text="📱 Устройства", callback_data=f"admin_campaign_edit_devices_{campaign_id}")])
    keyboard.append([InlineKeyboardButton(text="🌐 Серверы", callback_data=f"admin_campaign_edit_squads_{campaign_id}")])
    keyboard.append([InlineKeyboardButton(text="⬅️ Назад", callback_data=f"admin_campaign_manage_{campaign_id}")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_campaign_bonus_type_keyboard(language: str = "ru") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💰 Бонус на баланс", callback_data="campaign_bonus_balance")],
        [InlineKeyboardButton(text="📱 Бесплатная подписка", callback_data="campaign_bonus_subscription")],
        [InlineKeyboardButton(text="❌ Отмена", callback_data="admin_campaigns")]
    ])


def get_message_actions_keyboard(message_id: int, language: str = "ru") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🗑️ Удалить", callback_data=f"msg_delete_{message_id}")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="admin_messages")]
    ])


BROADCAST_BUTTON_ROWS = [
    ["balance", "subscription"],
    ["referrals", "promocode"],
    ["support", "connect"]
]

DEFAULT_BROADCAST_BUTTONS = {"balance", "subscription", "support"}


def get_broadcast_button_config(language: str = "ru") -> dict:
    return {
        "balance": {"text": "💰 Пополнить баланс", "callback": "balance_topup"},
        "subscription": {"text": "📱 Моя подписка", "callback": "menu_subscription"},
        "referrals": {"text": "🤝 Рефералы", "callback": "menu_referrals"},
        "promocode": {"text": "🎁 Промокод", "callback": "menu_promocode"},
        "support": {"text": "🆘 Поддержка", "callback": "menu_support"},
        "connect": {"text": "🔗 Подключиться", "callback": "subscription_connect"}
    }


def get_broadcast_button_labels(language: str = "ru") -> dict:
    return {
        "balance": "💰 Баланс",
        "subscription": "📱 Подписка",
        "referrals": "🤝 Рефералы",
        "promocode": "🎁 Промокод",
        "support": "🆘 Поддержка",
        "connect": "🔗 Подключиться"
    }


def get_message_buttons_selector_keyboard(selected_buttons: list, language: str = "ru") -> InlineKeyboardMarkup:
    return get_updated_message_buttons_selector_keyboard(selected_buttons, language)


def get_updated_message_buttons_selector_keyboard(selected_buttons: list, language: str = "ru") -> InlineKeyboardMarkup:
    return get_updated_message_buttons_selector_keyboard_with_media(selected_buttons, False, language)


def get_updated_message_buttons_selector_keyboard_with_media(selected_buttons: list, has_media: bool = False, language: str = "ru") -> InlineKeyboardMarkup:
    labels = get_broadcast_button_labels(language)
    keyboard = []
    for row in BROADCAST_BUTTON_ROWS:
        btn_row = []
        for key in row:
            is_selected = key in selected_buttons
            text = f"{'✅' if is_selected else '⬜'} {labels.get(key, key)}"
            btn_row.append(InlineKeyboardButton(text=text, callback_data=f"broadcast_btn_toggle_{key}"))
        keyboard.append(btn_row)
    if has_media:
        keyboard.append([InlineKeyboardButton(text="🖼️ Убрать медиа", callback_data="broadcast_remove_media")])
    else:
        keyboard.append([InlineKeyboardButton(text="🖼️ Добавить медиа", callback_data="broadcast_add_media")])
    keyboard.append([
        InlineKeyboardButton(text="✅ Продолжить", callback_data="broadcast_continue"),
        InlineKeyboardButton(text="❌ Отмена", callback_data="admin_messages")
    ])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_media_confirm_keyboard(language: str = "ru") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Подтвердить", callback_data="broadcast_media_confirm")],
        [InlineKeyboardButton(text="🔄 Изменить", callback_data="broadcast_media_change")],
        [InlineKeyboardButton(text="❌ Отмена", callback_data="admin_messages")]
    ])


def get_promocode_type_keyboard(language: str = "ru") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💰 Бонус на баланс", callback_data="promo_type_balance")],
        [InlineKeyboardButton(text="📅 Дни подписки", callback_data="promo_type_subscription_days")],
        [InlineKeyboardButton(text="🎁 Триальная подписка", callback_data="promo_type_trial_subscription")],
        [InlineKeyboardButton(text="🏷️ Промогруппа", callback_data="promo_type_promo_group")],
        [InlineKeyboardButton(text="❌ Отмена", callback_data="admin_promocodes")]
    ])


def get_referral_contest_manage_keyboard(contest_id: int, is_active: bool = True, language: str = "ru") -> InlineKeyboardMarkup:
    toggle_text = "⏸️ Отключить" if is_active else "▶️ Включить"
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✏️ Редактировать", callback_data=f"admin_contest_edit_{contest_id}")],
        [InlineKeyboardButton(text=toggle_text, callback_data=f"admin_contest_toggle_{contest_id}")],
        [InlineKeyboardButton(text="📊 Лидерборд", callback_data=f"admin_contest_leaderboard_{contest_id}")],
        [InlineKeyboardButton(text="📢 Отправить сводку", callback_data=f"admin_contest_send_summary_{contest_id}")],
        [InlineKeyboardButton(text="🗑️ Удалить", callback_data=f"admin_contest_delete_{contest_id}")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="admin_contests")]
    ])


def get_daily_contest_manage_keyboard(template_id: int, is_enabled: bool = True, language: str = "ru") -> InlineKeyboardMarkup:
    toggle_text = "⏸️ Отключить" if is_enabled else "▶️ Включить"
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=toggle_text, callback_data=f"admin_daily_toggle_{template_id}")],
        [InlineKeyboardButton(text="▶️ Запустить раунд", callback_data=f"admin_daily_start_{template_id}")],
        [InlineKeyboardButton(text="⏹️ Закрыть раунд", callback_data=f"admin_daily_close_{template_id}")],
        [InlineKeyboardButton(text="♻️ Сбросить попытки", callback_data=f"admin_daily_reset_attempts_{template_id}")],
        [InlineKeyboardButton(text="✏️ Настройки", callback_data=f"admin_daily_settings_{template_id}")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="admin_daily_contests")]
    ])


def get_contest_mode_keyboard(language: str = "ru") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎯 Реферальный конкурс", callback_data="contest_mode_referral")],
        [InlineKeyboardButton(text="📅 Ежедневный конкурс", callback_data="contest_mode_daily")],
        [InlineKeyboardButton(text="❌ Отмена", callback_data="admin_contests")]
    ])


def get_custom_criteria_keyboard(language: str = "ru") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💰 Минимальный баланс", callback_data="criteria_min_balance")],
        [InlineKeyboardButton(text="📅 Дата регистрации", callback_data="criteria_registration_date")],
        [InlineKeyboardButton(text="🕒 Последняя активность", callback_data="criteria_last_activity")],
        [InlineKeyboardButton(text="📶 Использованный трафик", callback_data="criteria_traffic_used")],
        [InlineKeyboardButton(text="🏷️ Промогруппа", callback_data="criteria_promo_group")],
        [InlineKeyboardButton(text="✅ Продолжить", callback_data="criteria_continue")],
        [InlineKeyboardButton(text="❌ Отмена", callback_data="admin_messages")]
    ])


def get_edit_prompt_keyboard(language: str = "ru") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="❌ Отмена", callback_data="admin_panel")]
    ])


def get_top_keyboard(language: str = "ru") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔄 Обновить", callback_data="admin_top_refresh")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="admin_panel")]
    ])
