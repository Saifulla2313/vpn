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
from app.handlers import start, profile, subscription, payment, admin

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
    dp.include_router(admin.router)
    
    logger.info("Bot started polling...")
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


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
    
    async with AsyncSessionLocal() as db:
        user = await get_user_by_telegram_id(db, telegram_id)
        if not user:
            return JSONResponse({"error": "User not found"}, status_code=404)
        
        subscription = await get_subscription_by_user_id(db, user.id)
        
        return {
            "telegram_id": user.telegram_id,
            "username": user.username,
            "balance": user.balance,
            "subscription": {
                "status": subscription.status.value if subscription else "inactive",
                "expires_at": subscription.expires_at.isoformat() if subscription and subscription.expires_at else None,
                "days_paid": subscription.days_paid if subscription else 0,
                "daily_price": subscription.daily_price if subscription else 6.0
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
            
            if user:
                subscription = await get_subscription_by_user_id(db, user.id)
                if subscription and subscription.status != SubscriptionStatus.ACTIVE:
                    if user.balance >= settings.SUBSCRIPTION_DAILY_PRICE:
                        days = int(user.balance // settings.SUBSCRIPTION_DAILY_PRICE)
                        await activate_subscription(db, user.id, days)
                
                if bot:
                    try:
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


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
