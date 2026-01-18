from datetime import datetime
from typing import Optional, List, Dict, Any
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models import SystemSettings


async def get_setting(db: AsyncSession, key: str) -> Optional[str]:
    result = await db.execute(
        select(SystemSettings).where(SystemSettings.key == key)
    )
    setting = result.scalar_one_or_none()
    return setting.value if setting else None


async def set_setting(db: AsyncSession, key: str, value: str) -> SystemSettings:
    result = await db.execute(
        select(SystemSettings).where(SystemSettings.key == key)
    )
    existing = result.scalar_one_or_none()
    
    if existing:
        existing.value = value
        existing.updated_at = datetime.utcnow()
        await db.commit()
        await db.refresh(existing)
        return existing
    
    setting = SystemSettings(key=key, value=value)
    db.add(setting)
    await db.commit()
    await db.refresh(setting)
    return setting


async def delete_setting(db: AsyncSession, key: str) -> bool:
    result = await db.execute(
        select(SystemSettings).where(SystemSettings.key == key)
    )
    setting = result.scalar_one_or_none()
    if not setting:
        return False
    await db.delete(setting)
    await db.commit()
    return True


async def get_all_settings(db: AsyncSession) -> Dict[str, str]:
    result = await db.execute(select(SystemSettings))
    settings = result.scalars().all()
    return {s.key: s.value for s in settings}


async def get_settings_by_prefix(db: AsyncSession, prefix: str) -> Dict[str, str]:
    result = await db.execute(
        select(SystemSettings).where(SystemSettings.key.startswith(prefix))
    )
    settings = result.scalars().all()
    return {s.key: s.value for s in settings}


async def bulk_set_settings(db: AsyncSession, settings: Dict[str, str]) -> None:
    for key, value in settings.items():
        await set_setting(db, key, value)


async def delete_system_setting(db: AsyncSession, key: str) -> bool:
    """Alias for delete_setting."""
    return await delete_setting(db, key)


async def upsert_system_setting(db: AsyncSession, key: str, value: str) -> SystemSettings:
    """Alias for set_setting."""
    return await set_setting(db, key, value)
