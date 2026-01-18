# VPN Bot Service

## Overview

This is a Telegram VPN subscription bot built with Python. The bot manages VPN subscriptions through the RemnaWave VPN panel, handles payments via multiple payment providers (YooKassa, CryptoBot, MulenPay, Platega, Pal24, WATA, Heleket), and provides admin functionality for user management, broadcasting, and analytics.

The system follows a modular architecture with clear separation between handlers (user interactions), services (business logic), database operations (CRUD), and external integrations (payment gateways, VPN panel).

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Core Framework
- **Bot Framework**: aiogram 3.x (async Telegram Bot API wrapper)
- **Web Framework**: FastAPI for webhook endpoints and admin API
- **Database**: PostgreSQL with SQLAlchemy async ORM (asyncpg driver)
- **Caching**: Redis for session storage, rate limiting, and user carts

### Application Structure
```
app/
├── handlers/       # Telegram command and callback handlers
├── services/       # Business logic layer (payments, subscriptions, etc.)
├── database/       # SQLAlchemy models and CRUD operations
├── external/       # Third-party API clients
├── middlewares/    # Request processing (auth, throttling, logging)
├── keyboards/      # Telegram inline keyboard builders
├── localization/   # Multi-language text templates
└── utils/          # Helpers (formatting, caching, decorators)
```

### Key Design Patterns

1. **Middleware Chain**: Requests flow through auth, throttling, logging, and maintenance middlewares before reaching handlers
2. **Service Layer**: All business logic isolated in services; handlers remain thin
3. **Repository Pattern**: Database operations abstracted in `database/crud/` modules
4. **Async Context Managers**: Used for database sessions and external API clients

### Bot Flow
1. User starts bot → creates/retrieves user record
2. User can deposit balance via multiple payment providers
3. Balance is used to purchase/extend VPN subscriptions
4. Subscriptions sync with RemnaWave panel for VPN access

### Payment Processing
- Webhook endpoints receive payment confirmations
- Each provider has dedicated service class with signature verification
- Transactions recorded with status tracking (pending → completed/failed)

### Subscription Management
- Integrates with RemnaWave VPN panel API
- Automatic subscription extension when balance sufficient
- Trial period support with configurable duration
- Promo codes and referral system for discounts

## External Dependencies

### Payment Providers
- **YooKassa**: Primary Russian payment gateway (yookassa SDK)
- **CryptoBot**: Telegram cryptocurrency payments
- **MulenPay**: Alternative crypto payments
- **Platega**: International payments
- **Pal24 (PayPalych)**: Russian alternative
- **WATA**: Additional payment option
- **Heleket**: Crypto payment integration
- **Telegram Stars**: Native Telegram payments

### VPN Panel
- **RemnaWave**: VPN panel for user provisioning and subscription management
  - Creates/manages VPN users
  - Controls access expiration
  - Syncs server/squad assignments

### Infrastructure
- **PostgreSQL**: Primary data store (users, subscriptions, transactions)
- **Redis**: Session storage, caching, rate limiting, user carts
- **Telegram Bot API**: Core bot functionality

### Configuration
All secrets and configuration loaded from environment variables via `app/config.py`:
- `BOT_TOKEN`: Telegram bot token
- `DATABASE_URL`: PostgreSQL connection string
- `REDIS_URL`: Redis connection string
- `REMNAWAVE_URL`, `REMNAWAVE_API_KEY`: VPN panel credentials
- `YOOKASSA_SHOP_ID`, `YOOKASSA_SECRET_KEY`: Payment credentials
- Various webhook secrets for payment verification

## Admin Panel

The comprehensive admin panel is located in `app/handlers/admin/` with 30+ modules organized into 6 submenus:

### 1. Users Submenu (`admin_submenu_users`)
- **users.py** - User search, list, management
- **subscriptions.py** - Subscription management
- **trials.py** - Trial period management
- **blacklist.py** - User blacklist
- **bulk_ban.py** - Mass ban operations

### 2. Promo & Statistics Submenu (`admin_submenu_promo`)
- **promocodes.py** - Promo code CRUD
- **statistics.py** - User/revenue stats
- **promo_groups.py** - Promo group management
- **promo_offers.py** - Special offers
- **referrals.py** - Referral system
- **payments.py** - Payment method management

### 3. Communications Submenu (`admin_submenu_communications`)
- **messages.py** - Broadcast messaging
- **welcome_text.py** - Welcome message config
- **polls.py** - User polls
- **contests.py** - Contests management
- **daily_contests.py** - Daily contests
- **campaigns.py** - Marketing campaigns

### 4. Support Submenu (`admin_submenu_support`)
- **tickets.py** - Support ticket system
- **faq.py** - FAQ management
- **rules.py** - Service rules
- **support_settings.py** - Support configuration

### 5. Settings Submenu (`admin_submenu_settings`)
- **bot_configuration.py** - Bot settings
- **tariffs.py** - Pricing plans
- **servers.py** - VPN server management
- **remnawave.py** - VPN panel integration
- **privacy_policy.py** - Privacy policy
- **public_offer.py** - Terms of service

### 6. System Submenu (`admin_submenu_system`)
- **monitoring.py** - System monitoring
- **backup.py** - Database backups
- **maintenance.py** - Maintenance mode
- **system_logs.py** - Log viewer
- **updates.py** - Version updates
- **reports.py** - System reports

### Admin Panel Entry
- Entry point: `app/handlers/admin/main.py`
- Keyboards: `app/keyboards/admin.py`
- States: `app/states.py` (AdminStates, TicketStates, etc.)

## Recent Changes (January 2026)

- Integrated comprehensive admin panel with 30+ modules
- Added 60+ database models for full functionality
- Added 70+ keyboard builder functions
- Added all necessary FSM states for admin workflows
- Added CRUD operations for all new models
- Added stub services for pending integrations