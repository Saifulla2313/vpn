from aiogram.fsm.state import State, StatesGroup


class AdminStates(StatesGroup):
    adding_traffic = State()
    confirming_pinned_broadcast = State()
    creating_campaign_balance = State()
    creating_campaign_bonus = State()
    creating_campaign_name = State()
    creating_campaign_start = State()
    creating_campaign_subscription_days = State()
    creating_campaign_subscription_devices = State()
    creating_campaign_subscription_servers = State()
    creating_campaign_subscription_traffic = State()
    creating_faq_content = State()
    creating_faq_title = State()
    creating_promocode = State()
    creating_promo_group_auto_assign = State()
    creating_promo_group_device_discount = State()
    creating_promo_group_name = State()
    creating_promo_group_period_discount = State()
    creating_promo_group_priority = State()
    creating_promo_group_server_discount = State()
    creating_promo_group_traffic_discount = State()
    creating_referral_contest_description = State()
    creating_referral_contest_end = State()
    creating_referral_contest_mode = State()
    creating_referral_contest_prize = State()
    creating_referral_contest_start = State()
    creating_referral_contest_time = State()
    creating_referral_contest_title = State()
    creating_tariff_devices = State()
    creating_tariff_name = State()
    creating_tariff_prices = State()
    creating_tariff_tier = State()
    creating_tariff_traffic = State()
    editing_campaign_balance = State()
    editing_campaign_name = State()
    editing_campaign_start = State()
    editing_campaign_subscription_days = State()
    editing_campaign_subscription_devices = State()
    editing_campaign_subscription_servers = State()
    editing_campaign_subscription_traffic = State()
    editing_daily_contest_field = State()
    editing_daily_contest_value = State()
    editing_faq_content = State()
    editing_faq_title = State()
    editing_notification_value = State()
    editing_pinned_message = State()
    editing_privacy_policy = State()
    editing_promo_group_auto_assign = State()
    editing_promo_group_device_discount = State()
    editing_promo_group_menu = State()
    editing_promo_group_name = State()
    editing_promo_group_period_discount = State()
    editing_promo_group_priority = State()
    editing_promo_group_server_discount = State()
    editing_promo_group_traffic_discount = State()
    editing_promo_offer_active_duration = State()
    editing_promo_offer_button = State()
    editing_promo_offer_discount = State()
    editing_promo_offer_message = State()
    editing_promo_offer_test_duration = State()
    editing_promo_offer_valid_hours = State()
    editing_public_offer = State()
    editing_referral_contest_summary_times = State()
    editing_rules_page = State()
    editing_server_country = State()
    editing_server_description = State()
    editing_server_limit = State()
    editing_server_name = State()
    editing_server_price = State()
    editing_server_promo_groups = State()
    editing_tariff_daily_price = State()
    editing_tariff_description = State()
    editing_tariff_device_price = State()
    editing_tariff_devices = State()
    editing_tariff_max_topup_traffic = State()
    editing_tariff_name = State()
    editing_tariff_prices = State()
    editing_tariff_tier = State()
    editing_tariff_traffic = State()
    editing_tariff_traffic_topup_packages = State()
    editing_tariff_trial_days = State()
    editing_user_balance = State()
    editing_user_devices = State()
    editing_user_referral_percent = State()
    editing_user_referrals = State()
    editing_user_restriction_reason = State()
    editing_user_traffic = State()
    editing_welcome_text = State()
    extending_subscription = State()
    granting_subscription = State()
    searching_promo_offer_user = State()
    selecting_promo_group = State()
    selecting_promo_offer_user = State()
    sending_user_message = State()
    setting_promocode_expiry = State()
    setting_promocode_uses = State()
    setting_promocode_value = State()
    test_referral_earning_input = State()
    viewing_user_from_balance_list = State()
    viewing_user_from_campaign_list = State()
    viewing_user_from_last_activity_list = State()
    viewing_user_from_purchases_list = State()
    viewing_user_from_ready_to_renew_list = State()
    viewing_user_from_spending_list = State()
    viewing_user_from_traffic_list = State()
    waiting_for_broadcast_media = State()
    waiting_for_broadcast_message = State()
    waiting_for_bulk_ban_list = State()
    waiting_for_user_search = State()


class BlacklistStates(StatesGroup):
    waiting_for_blacklist_url = State()


class BotConfigStates(StatesGroup):
    waiting_for_import_file = State()
    waiting_for_search_query = State()
    waiting_for_value = State()


class PricingStates(StatesGroup):
    waiting_for_value = State()


class SupportSettingsStates(StatesGroup):
    waiting_for_desc = State()


class TicketStates(StatesGroup):
    waiting_for_block_duration = State()
    waiting_for_reply = State()


class RemnaWaveSyncStates(StatesGroup):
    waiting_for_confirmation = State()
    syncing = State()
    waiting_for_schedule = State()


class SquadRenameStates(StatesGroup):
    waiting_for_name = State()
    waiting_for_new_name = State()


class SquadCreateStates(StatesGroup):
    waiting_for_name = State()
    waiting_for_description = State()
    waiting_for_servers = State()
    selecting_inbounds = State()


class SquadMigrationStates(StatesGroup):
    waiting_for_source = State()
    waiting_for_target = State()
    waiting_for_confirmation = State()
    selecting_source = State()
    selecting_target = State()
    confirming = State()


class AdminTicketStates(StatesGroup):
    waiting_for_reply = State()
    waiting_for_close_reason = State()
    viewing_ticket = State()
    waiting_for_block_duration = State()
