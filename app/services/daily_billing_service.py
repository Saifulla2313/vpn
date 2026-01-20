import asyncio
import logging
from dataclasses import dataclass
from datetime import datetime, timedelta, time, date
from typing import Any, Dict, List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.database.database import AsyncSessionLocal
from app.database.models import User, Subscription, SubscriptionStatus
from app.remnawave_api import RemnaWaveAPI


logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class DailyBillingStatus:
    enabled: bool
    billing_time: time
    next_run: Optional[datetime]
    last_run: Optional[datetime]
    last_run_success: Optional[bool]
    last_run_error: Optional[str]
    users_charged: int
    users_disabled: int
    is_running: bool


class DailyBillingService:
    def __init__(self) -> None:
        self._scheduler_task: Optional[asyncio.Task] = None
        self._scheduler_lock = asyncio.Lock()
        self._billing_lock = asyncio.Lock()
        
        self._loop: Optional[asyncio.AbstractEventLoop] = None
        self._initialized = False
        
        self._next_run: Optional[datetime] = None
        self._last_run: Optional[datetime] = None
        self._last_run_success: Optional[bool] = None
        self._last_run_error: Optional[str] = None
        self._last_users_charged: int = 0
        self._last_users_disabled: int = 0
        self._is_running: bool = False
    
    async def initialize(self) -> None:
        self._loop = asyncio.get_running_loop()
        self._initialized = True
        await self.refresh_schedule()
    
    async def refresh_schedule(self) -> None:
        async with self._scheduler_lock:
            if self._scheduler_task and not self._scheduler_task.done():
                self._scheduler_task.cancel()
                try:
                    await self._scheduler_task
                except asyncio.CancelledError:
                    pass
                finally:
                    self._scheduler_task = None
            
            billing_time_str = getattr(settings, 'DAILY_BILLING_TIME', '00:05')
            try:
                hour, minute = map(int, billing_time_str.split(':'))
                billing_time = time(hour, minute)
            except (ValueError, AttributeError):
                billing_time = time(0, 5)
            
            self._scheduler_task = asyncio.create_task(self._run_scheduler(billing_time))
    
    async def stop(self) -> None:
        async with self._scheduler_lock:
            if self._scheduler_task and not self._scheduler_task.done():
                self._scheduler_task.cancel()
                try:
                    await self._scheduler_task
                except asyncio.CancelledError:
                    pass
            self._scheduler_task = None
            self._next_run = None
    
    def get_status(self) -> DailyBillingStatus:
        billing_time_str = getattr(settings, 'DAILY_BILLING_TIME', '00:05')
        try:
            hour, minute = map(int, billing_time_str.split(':'))
            billing_time = time(hour, minute)
        except (ValueError, AttributeError):
            billing_time = time(0, 5)
        return DailyBillingStatus(
            enabled=True,
            billing_time=billing_time,
            next_run=self._next_run,
            last_run=self._last_run,
            last_run_success=self._last_run_success,
            last_run_error=self._last_run_error,
            users_charged=self._last_users_charged,
            users_disabled=self._last_users_disabled,
            is_running=self._is_running
        )
    
    async def _run_scheduler(self, billing_time: time) -> None:
        while True:
            try:
                now = datetime.utcnow()
                next_run = datetime.combine(now.date(), billing_time)
                
                if next_run <= now:
                    next_run = next_run + timedelta(days=1)
                
                self._next_run = next_run
                sleep_seconds = (next_run - now).total_seconds()
                
                logger.info(f"Daily billing scheduled for {next_run} (in {sleep_seconds:.0f}s)")
                await asyncio.sleep(sleep_seconds)
                
                await self.run_daily_billing()
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Scheduler error: {e}")
                await asyncio.sleep(60)
    
    async def run_daily_billing(self) -> Dict[str, Any]:
        if self._is_running:
            return {"status": "already_running"}
        
        async with self._billing_lock:
            self._is_running = True
            self._last_run = datetime.utcnow()
            
            users_charged = 0
            users_disabled = 0
            errors = []
            
            try:
                async with AsyncSessionLocal() as db:
                    result = await db.execute(
                        select(User).where(
                            User.remnawave_uuid.isnot(None),
                            User.balance > 0
                        )
                    )
                    users = result.scalars().all()
                    
                    logger.info(f"Daily billing: processing {len(users)} users with balance")
                    
                    async with RemnaWaveAPI(
                        base_url=settings.REMNAWAVE_URL, 
                        api_key=settings.REMNAWAVE_API_KEY
                    ) as api:
                        for user in users:
                            try:
                                charged = await self._charge_user(db, api, user)
                                if charged:
                                    users_charged += 1
                            except Exception as e:
                                logger.error(f"Error charging user {user.telegram_id}: {e}")
                                errors.append(str(e))
                    
                    result = await db.execute(
                        select(User).where(
                            User.remnawave_uuid.isnot(None),
                            User.balance <= 0
                        )
                    )
                    zero_balance_users = result.scalars().all()
                    
                    async with RemnaWaveAPI(
                        base_url=settings.REMNAWAVE_URL, 
                        api_key=settings.REMNAWAVE_API_KEY
                    ) as api:
                        for user in zero_balance_users:
                            try:
                                disabled = await self._disable_user_if_expired(db, api, user)
                                if disabled:
                                    users_disabled += 1
                            except Exception as e:
                                logger.error(f"Error disabling user {user.telegram_id}: {e}")
                                errors.append(str(e))
                
                self._last_run_success = True
                self._last_run_error = None
                self._last_users_charged = users_charged
                self._last_users_disabled = users_disabled
                
                logger.info(f"Daily billing complete: {users_charged} charged, {users_disabled} disabled")
                
                return {
                    "status": "ok",
                    "users_charged": users_charged,
                    "users_disabled": users_disabled,
                    "errors": errors
                }
                
            except Exception as e:
                self._last_run_success = False
                self._last_run_error = str(e)
                logger.error(f"Daily billing failed: {e}")
                return {"status": "error", "error": str(e)}
            finally:
                self._is_running = False
    
    async def _charge_user(self, db: AsyncSession, api: RemnaWaveAPI, user: User) -> bool:
        remnawave_user = await api.get_user_by_uuid(user.remnawave_uuid)
        if not remnawave_user:
            logger.warning(f"RemnaWave user not found for {user.telegram_id}")
            return False
        
        now = datetime.utcnow()
        expire_at = remnawave_user.expire_at
        if expire_at and expire_at.tzinfo:
            expire_at = expire_at.replace(tzinfo=None)
        
        if expire_at and expire_at < now:
            return False
        
        devices_info = await api.get_user_devices(user.remnawave_uuid)
        device_count = devices_info.get('total', 0)
        if device_count < 1:
            device_count = 1
        
        daily_price = settings.SUBSCRIPTION_DAILY_PRICE * device_count
        
        if user.balance < daily_price:
            return False
        
        user.balance -= daily_price
        await db.commit()
        
        new_expire = (expire_at or now) + timedelta(days=1)
        await api.update_user(
            uuid=user.remnawave_uuid,
            expire_at=new_expire
        )
        
        logger.info(f"Charged user {user.telegram_id}: -{daily_price}₽ ({device_count} devices), expire: {new_expire}")
        return True
    
    async def _disable_user_if_expired(self, db: AsyncSession, api: RemnaWaveAPI, user: User) -> bool:
        remnawave_user = await api.get_user_by_uuid(user.remnawave_uuid)
        if not remnawave_user:
            return False
        
        now = datetime.utcnow()
        expire_at = remnawave_user.expire_at
        if expire_at and expire_at.tzinfo:
            expire_at = expire_at.replace(tzinfo=None)
        
        if expire_at and expire_at < now:
            await api.update_user(
                uuid=user.remnawave_uuid,
                status="DISABLED"
            )
            
            result = await db.execute(
                select(Subscription).where(Subscription.user_id == user.id)
            )
            subscription = result.scalar_one_or_none()
            if subscription:
                subscription.status = SubscriptionStatus.EXPIRED
                await db.commit()
            
            logger.info(f"Disabled expired subscription for user {user.telegram_id}")
            return True
        
        return False


daily_billing_service = DailyBillingService()
