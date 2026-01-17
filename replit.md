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