import os
import asyncio
import logging
from contextlib import asynccontextmanager

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from app.config import settings
from app.database.database import init_db, AsyncSessionLocal
from app.handlers import start, profile, subscription, payment
from app.handlers.admin import main as admin_main
from app.handlers.admin import (
    monitoring, promocodes, users, subscriptions, tickets, 
    statistics, blacklist, payments, referrals, servers,
    maintenance, backup, promo_groups, promo_offers,
    campaigns, messages, polls, contests, daily_contests,
    welcome_text, faq, rules, privacy_policy, public_offer,
    bot_configuration, tariffs, remnawave, system_logs, 
    updates, reports, bulk_ban, trials, user_messages
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

bot: Bot = None
dp: Dispatcher = None


class DatabaseMiddleware:
    def __init__(self, dp: Dispatcher):
        dp.update.middleware(self)
    
    async def __call__(self, handler, event, data):
        async with AsyncSessionLocal() as session:
            data["db"] = session
            return await handler(event, data)


async def start_bot():
    global bot, dp
    
    try:
        if not settings.BOT_TOKEN:
            logger.error("BOT_TOKEN is not set!")
            return
        
        bot = Bot(
            token=settings.BOT_TOKEN,
            default=DefaultBotProperties(parse_mode=ParseMode.HTML)
        )
        
        dp = Dispatcher(storage=MemoryStorage())
        
        DatabaseMiddleware(dp)
        
        dp.include_router(start.router)
        dp.include_router(profile.router)
        dp.include_router(subscription.router)
        dp.include_router(payment.router)
        
        admin_main.register_handlers(dp)
        monitoring.register_handlers(dp)
        promocodes.register_handlers(dp)
        users.register_handlers(dp)
        subscriptions.register_handlers(dp)
        tickets.register_handlers(dp)
        statistics.register_handlers(dp)
        blacklist.register_handlers(dp)
        payments.register_handlers(dp)
        referrals.register_handlers(dp)
        servers.register_handlers(dp)
        maintenance.register_handlers(dp)
        backup.register_handlers(dp)
        promo_groups.register_handlers(dp)
        promo_offers.register_handlers(dp)
        campaigns.register_handlers(dp)
        messages.register_handlers(dp)
        polls.register_handlers(dp)
        contests.register_handlers(dp)
        daily_contests.register_handlers(dp)
        welcome_text.register_handlers(dp)
        faq.register_handlers(dp)
        rules.register_handlers(dp)
        privacy_policy.register_handlers(dp)
        public_offer.register_handlers(dp)
        bot_configuration.register_handlers(dp)
        tariffs.register_handlers(dp)
        remnawave.register_handlers(dp)
        system_logs.register_handlers(dp)
        updates.register_handlers(dp)
        reports.register_handlers(dp)
        bulk_ban.register_handlers(dp)
        trials.register_handlers(dp)
        user_messages.register_handlers(dp)
        
        logger.info("Bot started polling...")
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    except Exception as e:
        logger.error(f"Bot polling error: {e}", exc_info=True)


async def stop_bot():
    global bot, dp
    if dp:
        await dp.stop_polling()
    if bot:
        await bot.session.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    logger.info("Database initialized")
    
    bot_task = asyncio.create_task(start_bot())
    
    yield
    
    await stop_bot()
    bot_task.cancel()
    try:
        await bot_task
    except asyncio.CancelledError:
        pass


app = FastAPI(title="VPN Bot", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>VPN Bot</title>
        <meta charset="utf-8">
        <style>
            body { font-family: Arial, sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
            .container { text-align: center; color: white; }
            h1 { font-size: 3em; margin-bottom: 20px; }
            p { font-size: 1.2em; opacity: 0.9; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>VPN Bot</h1>
            <p>Telegram бот для продажи VPN подписок</p>
        </div>
    </body>
    </html>
    """


@app.get("/health")
async def health():
    return {"status": "ok", "bot_running": bot is not None}


@app.get("/miniapp", response_class=HTMLResponse)
async def miniapp():
    with open("static/miniapp/index.html", "r", encoding="utf-8") as f:
        return f.read()


@app.get("/api/user/{telegram_id}")
async def get_user_api(telegram_id: int):
    from app.database.crud.user import get_user_by_telegram_id
    from app.database.crud.subscription import get_subscription_by_user_id
    from app.remnawave_api import RemnaWaveAPI
    from datetime import datetime
    import math
    
    async with AsyncSessionLocal() as db:
        user = await get_user_by_telegram_id(db, telegram_id)
        if not user:
            return JSONResponse({"error": "User not found"}, status_code=404)
        
        subscription = await get_subscription_by_user_id(db, user.id)
        
        days_left = 0
        expires_at = None
        device_count = 1
        
        if user.remnawave_uuid:
            try:
                async with RemnaWaveAPI(base_url=settings.REMNAWAVE_URL, api_key=settings.REMNAWAVE_API_KEY) as api:
                    remnawave_user = await api.get_user_by_uuid(user.remnawave_uuid)
                    if remnawave_user and remnawave_user.expire_at:
                        expires_at = remnawave_user.expire_at
                        now = datetime.utcnow()
                        # Make both timezone-naive for comparison
                        if expires_at.tzinfo is not None:
                            expires_at_naive = expires_at.replace(tzinfo=None)
                        else:
                            expires_at_naive = expires_at
                        if expires_at_naive > now:
                            diff = expires_at_naive - now
                            days_left = math.ceil(diff.total_seconds() / 86400)
                        else:
                            days_left = 0
                    if remnawave_user:
                        device_count = remnawave_user.hwid_device_limit or 1
            except Exception as e:
                logger.warning(f"Failed to fetch RemnaWave user: {e}")
                if subscription and subscription.expires_at:
                    expires_at = subscription.expires_at
                    now = datetime.utcnow()
                    if expires_at > now:
                        diff = expires_at - now
                        days_left = math.ceil(diff.total_seconds() / 86400)
        
        daily_price = settings.SUBSCRIPTION_DAILY_PRICE
        total_daily_price = daily_price * device_count
        
        return {
            "telegram_id": user.telegram_id,
            "username": user.username,
            "balance": user.balance,
            "subscription": {
                "status": subscription.status.value if subscription else "inactive",
                "expires_at": expires_at.isoformat() if expires_at else None,
                "days_left": days_left,
                "daily_price": total_daily_price,
                "device_count": device_count,
                "price_per_device": daily_price
            } if subscription else None,
            "remnawave_uuid": user.remnawave_uuid,
            "trial_used": user.trial_used
        }


@app.post("/api/webhook/yookassa")
async def yookassa_webhook(request: Request):
    from app.database.crud.user import get_user_by_id, update_user_balance
    from app.database.crud.transaction import get_transaction_by_payment_id, complete_transaction
    from app.database.crud.subscription import get_subscription_by_user_id, activate_subscription
    from app.database.models import SubscriptionStatus
    from app.remnawave_api import RemnaWaveAPI
    from datetime import timedelta
    
    try:
        data = await request.json()
        logger.info(f"YooKassa webhook: {data}")
        
        if data.get("event") != "payment.succeeded":
            return {"status": "ignored"}
        
        payment_obj = data.get("object", {})
        payment_id = payment_obj.get("id")
        
        if not payment_id:
            return {"status": "error", "message": "No payment ID"}
        
        async with AsyncSessionLocal() as db:
            transaction = await get_transaction_by_payment_id(db, payment_id)
            if not transaction:
                logger.warning(f"Transaction not found for payment {payment_id}")
                return {"status": "error", "message": "Transaction not found"}
            
            if transaction.status.value == "completed":
                return {"status": "already_processed"}
            
            await complete_transaction(db, transaction.id)
            user = await update_user_balance(db, transaction.user_id, transaction.amount)
            
            days_added = 0
            if user and user.remnawave_uuid and user.balance > 0:
                try:
                    async with RemnaWaveAPI(base_url=settings.REMNAWAVE_URL, api_key=settings.REMNAWAVE_API_KEY) as api:
                        remnawave_user = await api.get_user_by_uuid(user.remnawave_uuid)
                        if remnawave_user:
                            device_count = remnawave_user.hwid_device_limit or 1
                            daily_price = settings.SUBSCRIPTION_DAILY_PRICE * device_count
                            
                            days_to_add = int(user.balance // daily_price)
                            if days_to_add > 0:
                                cost = days_to_add * daily_price
                                
                                current_expire = remnawave_user.expire_at
                                now = datetime.utcnow()
                                if current_expire and current_expire.tzinfo:
                                    current_expire = current_expire.replace(tzinfo=None)
                                
                                if current_expire and current_expire > now:
                                    new_expire = current_expire + timedelta(days=days_to_add)
                                else:
                                    new_expire = now + timedelta(days=days_to_add)
                                
                                await api.update_user(
                                    uuid=user.remnawave_uuid,
                                    expire_at=new_expire
                                )
                                
                                await update_user_balance(db, user.id, -cost)
                                days_added = days_to_add
                                logger.info(f"Extended subscription for user {user.telegram_id}: +{days_to_add} days, -{cost}₽")
                                
                                subscription = await get_subscription_by_user_id(db, user.id)
                                if subscription and subscription.status == SubscriptionStatus.TRIAL:
                                    subscription.status = SubscriptionStatus.ACTIVE
                                    await db.commit()
                                    logger.info(f"Changed subscription status from TRIAL to ACTIVE for user {user.telegram_id}")
                except Exception as e:
                    logger.error(f"Failed to auto-extend subscription: {e}")
            
            if user and not user.remnawave_uuid:
                subscription = await get_subscription_by_user_id(db, user.id)
                if subscription and subscription.status != SubscriptionStatus.ACTIVE:
                    if user.balance >= settings.SUBSCRIPTION_DAILY_PRICE:
                        days = int(user.balance // settings.SUBSCRIPTION_DAILY_PRICE)
                        await activate_subscription(db, user.id, days)
            
            if user and bot:
                try:
                    if days_added > 0:
                        await bot.send_message(
                            user.telegram_id,
                            f"✅ Оплата {transaction.amount}₽ получена!\n"
                            f"Подписка продлена на {days_added} дней"
                        )
                    else:
                        await bot.send_message(
                            user.telegram_id,
                            f"✅ Оплата {transaction.amount}₽ получена!\nВаш баланс: {user.balance}₽"
                        )
                except Exception as e:
                    logger.error(f"Failed to notify user: {e}")
        
        return {"status": "ok"}
    
    except Exception as e:
        logger.error(f"YooKassa webhook error: {e}")
        return {"status": "error", "message": str(e)}


@app.post("/api/trial/activate")
async def activate_trial_api(request: Request):
    """Activate trial subscription via miniapp"""
    from app.database.crud.user import get_user_by_telegram_id, mark_trial_used
    from app.database.crud.subscription import get_subscription_by_user_id, create_subscription
    from app.database.models import SubscriptionStatus
    from app.services.subscription_service import SubscriptionService
    
    try:
        data = await request.json()
        telegram_id = data.get("telegram_id")
        
        if not telegram_id:
            return JSONResponse({"error": "telegram_id required"}, status_code=400)
        
        async with AsyncSessionLocal() as db:
            user = await get_user_by_telegram_id(db, telegram_id)
            if not user:
                return JSONResponse({"error": "User not found"}, status_code=404)
            
            if user.trial_used:
                return JSONResponse({"error": "Trial already used"}, status_code=400)
            
            subscription_service = SubscriptionService()
            result = await subscription_service.activate_trial(db, user)
            
            if result.get("success"):
                return {"status": "ok", "message": "Trial activated", "key": result.get("subscription_key")}
            else:
                return JSONResponse({"error": result.get("error", "Failed to activate trial")}, status_code=500)
    
    except Exception as e:
        logger.error(f"Trial activation error: {e}")
        return JSONResponse({"error": str(e)}, status_code=500)


@app.post("/api/payment/create")
async def create_payment_api(request: Request):
    """Create payment link for miniapp"""
    from app.database.crud.user import get_user_by_telegram_id
    from app.database.crud.transaction import create_transaction
    from app.database.models import TransactionStatus
    from yookassa import Configuration, Payment as YooPayment
    import uuid
    
    try:
        data = await request.json()
        telegram_id = data.get("telegram_id")
        amount = data.get("amount", 300)
        
        if not telegram_id:
            return JSONResponse({"error": "telegram_id required"}, status_code=400)
        
        if amount < 50:
            return JSONResponse({"error": "Minimum amount is 50₽"}, status_code=400)
        
        async with AsyncSessionLocal() as db:
            user = await get_user_by_telegram_id(db, telegram_id)
            if not user:
                return JSONResponse({"error": "User not found"}, status_code=404)
            
            Configuration.account_id = settings.YOOKASSA_SHOP_ID
            Configuration.secret_key = settings.YOOKASSA_SECRET_KEY
            
            idempotence_key = str(uuid.uuid4())
            
            payment = YooPayment.create({
                "amount": {"value": str(amount), "currency": "RUB"},
                "confirmation": {"type": "redirect", "return_url": f"https://t.me/{settings.BOT_USERNAME}"},
                "capture": True,
                "description": f"Пополнение VPN баланса - {amount}₽",
                "metadata": {"telegram_id": telegram_id, "user_id": user.id},
                "receipt": {
                    "customer": {
                        "email": settings.YOOKASSA_DEFAULT_RECEIPT_EMAIL
                    },
                    "items": [
                        {
                            "description": "Пополнение баланса VPN",
                            "quantity": "1.00",
                            "amount": {
                                "value": str(amount),
                                "currency": "RUB"
                            },
                            "vat_code": settings.YOOKASSA_VAT_CODE,
                            "payment_mode": settings.YOOKASSA_PAYMENT_MODE,
                            "payment_subject": settings.YOOKASSA_PAYMENT_SUBJECT
                        }
                    ]
                }
            }, idempotence_key)
            
            await create_transaction(
                db,
                user_id=user.id,
                amount=float(amount),
                provider="yookassa",
                payment_id=payment.id,
                status=TransactionStatus.PENDING
            )
            
            return {
                "status": "ok",
                "payment_url": payment.confirmation.confirmation_url
            }
    
    except Exception as e:
        logger.error(f"Payment creation error: {e}")
        return JSONResponse({"error": str(e)}, status_code=500)


@app.get("/api/devices/{telegram_id}")
async def get_user_devices(telegram_id: int):
    """Get connected devices for miniapp"""
    from app.database.crud.user import get_user_by_telegram_id
    from app.remnawave_api import RemnaWaveAPI
    
    async with AsyncSessionLocal() as db:
        user = await get_user_by_telegram_id(db, telegram_id)
        if not user:
            return JSONResponse({"error": "User not found"}, status_code=404)
        
        if not user.remnawave_uuid:
            return {"devices": [], "total": 0}
        
        try:
            async with RemnaWaveAPI(base_url=settings.REMNAWAVE_URL, api_key=settings.REMNAWAVE_API_KEY) as api:
                devices_info = await api.get_user_devices(user.remnawave_uuid)
                devices = devices_info.get('devices', [])
                
                formatted_devices = []
                for device in devices:
                    formatted_devices.append({
                        "hwid": device.get('hwid', ''),
                        "user_agent": device.get('userAgent', device.get('user_agent', '')),
                        "added_at": device.get('addedAt', device.get('added_at', '')),
                        "online_at": device.get('onlineAt', device.get('online_at', ''))
                    })
                
                return {
                    "devices": formatted_devices,
                    "total": len(formatted_devices),
                    "price_per_device": settings.SUBSCRIPTION_DAILY_PRICE
                }
        except Exception as e:
            logger.error(f"Error fetching devices: {e}")
            return {"devices": [], "total": 0, "error": str(e)}


@app.delete("/api/devices/{telegram_id}/{device_hwid}")
async def remove_user_device(telegram_id: int, device_hwid: str):
    """Remove a device"""
    from app.database.crud.user import get_user_by_telegram_id
    from app.remnawave_api import RemnaWaveAPI
    
    async with AsyncSessionLocal() as db:
        user = await get_user_by_telegram_id(db, telegram_id)
        if not user:
            return JSONResponse({"error": "User not found"}, status_code=404)
        
        if not user.remnawave_uuid:
            return JSONResponse({"error": "No VPN account"}, status_code=400)
        
        try:
            async with RemnaWaveAPI(base_url=settings.REMNAWAVE_URL, api_key=settings.REMNAWAVE_API_KEY) as api:
                success = await api.remove_device(user.remnawave_uuid, device_hwid)
                if success:
                    return {"status": "ok", "message": "Device removed"}
                else:
                    return JSONResponse({"error": "Failed to remove device"}, status_code=500)
        except Exception as e:
            logger.error(f"Error removing device: {e}")
            return JSONResponse({"error": str(e)}, status_code=500)


@app.get("/api/subscription/key/{telegram_id}")
async def get_subscription_key(telegram_id: int):
    """Get VPN subscription key for miniapp"""
    from app.database.crud.user import get_user_by_telegram_id
    from app.database.crud.subscription import get_subscription_by_user_id
    from app.remnawave_api import RemnaWaveAPI
    
    async with AsyncSessionLocal() as db:
        user = await get_user_by_telegram_id(db, telegram_id)
        if not user:
            return JSONResponse({"error": "User not found"}, status_code=404)
        
        subscription = await get_subscription_by_user_id(db, user.id)
        if not subscription or subscription.status.value == "inactive":
            return JSONResponse({"error": "No active subscription"}, status_code=400)
        
        if not user.remnawave_uuid:
            return JSONResponse({"error": "VPN key not configured"}, status_code=400)
        
        try:
            async with RemnaWaveAPI(base_url=settings.REMNAWAVE_URL, api_key=settings.REMNAWAVE_API_KEY) as api:
                remnawave_user = await api.get_user_by_uuid(user.remnawave_uuid)
                
                if remnawave_user and remnawave_user.subscription_url:
                    return {
                        "status": "ok",
                        "key": remnawave_user.subscription_url,
                        "expires_at": subscription.expires_at.isoformat() if subscription.expires_at else None
                    }
                else:
                    return JSONResponse({"error": "VPN key not available"}, status_code=400)
        except Exception as e:
            logger.error(f"Error fetching VPN key: {e}")
            return JSONResponse({"error": "Failed to fetch VPN key"}, status_code=500)


@app.post("/miniapp/subscription")
async def miniapp_subscription(request: Request):
    """Get subscription data for miniapp via Telegram WebApp init_data"""
    from app.database.crud.user import get_user_by_telegram_id
    from app.database.crud.subscription import get_subscription_by_user_id
    from app.remnawave_api import RemnaWaveAPI
    from app.utils.telegram_webapp import parse_webapp_init_data, TelegramWebAppAuthError
    
    try:
        data = await request.json()
        init_data = data.get("init_data", "")
        
        try:
            webapp_data = parse_webapp_init_data(init_data, settings.BOT_TOKEN)
        except TelegramWebAppAuthError as e:
            return JSONResponse({"error": str(e)}, status_code=401)
        
        telegram_user = webapp_data.get("user", {})
        telegram_id = telegram_user.get("id")
        
        if not telegram_id:
            return JSONResponse({"error": "Invalid user data"}, status_code=400)
        
        async with AsyncSessionLocal() as db:
            user = await get_user_by_telegram_id(db, int(telegram_id))
            if not user:
                return JSONResponse({"error": "User not found"}, status_code=404)
            
            subscription = await get_subscription_by_user_id(db, user.id)
            subscription_key = None
            devices = []
            
            if user.remnawave_uuid:
                try:
                    async with RemnaWaveAPI(base_url=settings.REMNAWAVE_URL, api_key=settings.REMNAWAVE_API_KEY) as api:
                        remnawave_user = await api.get_user_by_uuid(user.remnawave_uuid)
                        if remnawave_user:
                            subscription_key = remnawave_user.subscription_url
                        
                        devices_info = await api.get_user_devices(user.remnawave_uuid)
                        if devices_info:
                            devices_list = devices_info.get('devices', [])
                            devices = [{"name": d.get("name", d.get("userAgent", "Device")[:20] if d.get("userAgent") else "Device"), "hwid": d.get("hwid")} for d in devices_list]
                except Exception as e:
                    logger.warning(f"Failed to fetch RemnaWave data: {e}")
            
            balance_kopeks = getattr(user, 'balance_kopeks', 0) or (int(getattr(user, 'balance', 0) * 100) if hasattr(user, 'balance') else 0)
            
            bot_username = "plus_vpnn_bot"
            referral_link = f"https://t.me/{bot_username}?start=ref{user.id}"
            
            daily_price = settings.SUBSCRIPTION_DAILY_PRICE
            
            return {
                "user": {
                    "id": user.id,
                    "telegram_id": user.telegram_id,
                    "balance_kopeks": balance_kopeks,
                },
                "subscription": {
                    "status": subscription.status.value if subscription else "inactive",
                    "expires_at": subscription.expires_at.isoformat() if subscription and subscription.expires_at else None,
                } if subscription else None,
                "subscription_key": subscription_key,
                "devices": devices,
                "referral_link": referral_link,
                "referral_count": getattr(user, 'referral_count', 0) or 0,
                "referral_earned": getattr(user, 'referral_earned', 0) or 0,
                "daily_price": daily_price,
            }
    except Exception as e:
        logger.error(f"Miniapp subscription error: {e}")
        return JSONResponse({"error": "Internal error"}, status_code=500)


@app.post("/miniapp/payments/create")
async def miniapp_create_payment(request: Request):
    """Create payment from miniapp"""
    from app.database.crud.user import get_user_by_telegram_id
    from app.database.crud.transaction import create_transaction
    from app.utils.telegram_webapp import parse_webapp_init_data, TelegramWebAppAuthError
    
    try:
        data = await request.json()
        init_data = data.get("init_data", "")
        amount_kopeks = data.get("amount_kopeks", 30000)
        
        try:
            webapp_data = parse_webapp_init_data(init_data, settings.BOT_TOKEN)
        except TelegramWebAppAuthError as e:
            return JSONResponse({"error": str(e)}, status_code=401)
        
        telegram_user = webapp_data.get("user", {})
        telegram_id = telegram_user.get("id")
        
        if not telegram_id:
            return JSONResponse({"error": "Invalid user data"}, status_code=400)
        
        amount_rubles = amount_kopeks / 100
        if amount_rubles < 50:
            return JSONResponse({"error": "Minimum amount is 50₽"}, status_code=400)
        
        async with AsyncSessionLocal() as db:
            user = await get_user_by_telegram_id(db, int(telegram_id))
            if not user:
                return JSONResponse({"error": "User not found"}, status_code=404)
            
            from yookassa import Configuration, Payment as YooPayment
            from uuid import uuid4
            
            Configuration.account_id = settings.YOOKASSA_SHOP_ID
            Configuration.secret_key = settings.YOOKASSA_SECRET_KEY
            
            idempotence_key = str(uuid4())
            return_url = settings.YOOKASSA_RETURN_URL or f"https://t.me/plus_vpnn_bot"
            
            from app.database.models import Transaction, TransactionType, PaymentMethod
            transaction = Transaction(
                user_id=user.id,
                amount=amount_rubles,
                type=TransactionType.deposit,
                payment_method=PaymentMethod.yookassa,
                status="pending",
                description=f"Пополнение баланса - {amount_rubles}₽"
            )
            db.add(transaction)
            await db.commit()
            await db.refresh(transaction)
            
            payment_data = {
                "amount": {"value": str(amount_rubles), "currency": "RUB"},
                "confirmation": {"type": "redirect", "return_url": return_url},
                "capture": True,
                "description": f"Пополнение VPN баланса - {amount_rubles}₽",
                "metadata": {
                    "user_id": str(user.id),
                    "telegram_id": str(telegram_id),
                    "transaction_id": str(transaction.id)
                },
                "receipt": {
                    "customer": {"email": "noreply@vpn.bot"},
                    "items": [{
                        "description": "Пополнение баланса VPN бота",
                        "quantity": "1.00",
                        "amount": {"value": str(amount_rubles), "currency": "RUB"},
                        "vat_code": "1",
                        "payment_mode": "full_payment",
                        "payment_subject": "service"
                    }]
                }
            }
            
            try:
                payment = YooPayment.create(payment_data, idempotence_key)
                
                transaction.external_id = payment.id
                await db.commit()
                
                return {
                    "payment_url": payment.confirmation.confirmation_url,
                    "payment_id": payment.id
                }
            except Exception as e:
                logger.error(f"YooKassa payment error: {e}")
                return JSONResponse({"error": "Payment creation failed"}, status_code=500)
                
    except Exception as e:
        logger.error(f"Miniapp payment error: {e}")
        return JSONResponse({"error": "Internal error"}, status_code=500)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
