from datetime import datetime
from typing import Optional, Dict, Any
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models import SystemSettings


PRIVACY_POLICY_KEY = "privacy_policy"


async def get_privacy_policy(db: AsyncSession) -> Optional[str]:
    result = await db.execute(
        select(SystemSettings).where(SystemSettings.key == PRIVACY_POLICY_KEY)
    )
    setting = result.scalar_one_or_none()
    return setting.value if setting else None


async def set_privacy_policy(db: AsyncSession, content: str) -> SystemSettings:
    result = await db.execute(
        select(SystemSettings).where(SystemSettings.key == PRIVACY_POLICY_KEY)
    )
    existing = result.scalar_one_or_none()
    
    if existing:
        existing.value = content
        existing.updated_at = datetime.utcnow()
        await db.commit()
        await db.refresh(existing)
        return existing
    
    setting = SystemSettings(key=PRIVACY_POLICY_KEY, value=content)
    db.add(setting)
    await db.commit()
    await db.refresh(setting)
    return setting


async def delete_privacy_policy(db: AsyncSession) -> bool:
    result = await db.execute(
        select(SystemSettings).where(SystemSettings.key == PRIVACY_POLICY_KEY)
    )
    setting = result.scalar_one_or_none()
    if not setting:
        return False
    await db.delete(setting)
    await db.commit()
    return True


async def get_privacy_policy_info(db: AsyncSession) -> Dict[str, Any]:
    result = await db.execute(
        select(SystemSettings).where(SystemSettings.key == PRIVACY_POLICY_KEY)
    )
    setting = result.scalar_one_or_none()
    
    if not setting:
        return {
            'exists': False,
            'content': None,
            'updated_at': None
        }
    
    return {
        'exists': True,
        'content': setting.value,
        'updated_at': setting.updated_at
    }


PRIVACY_POLICY_ENABLED_KEY = "privacy_policy_enabled"


async def set_privacy_policy_enabled(db: AsyncSession, enabled: bool) -> bool:
    """Set privacy policy enabled status."""
    result = await db.execute(
        select(SystemSettings).where(SystemSettings.key == PRIVACY_POLICY_ENABLED_KEY)
    )
    existing = result.scalar_one_or_none()
    
    if existing:
        existing.value = str(enabled).lower()
        existing.updated_at = datetime.utcnow()
    else:
        setting = SystemSettings(key=PRIVACY_POLICY_ENABLED_KEY, value=str(enabled).lower())
        db.add(setting)
    
    await db.commit()
    return True


async def upsert_privacy_policy(
    db: AsyncSession,
    content: str,
    language: str = "ru",
    **kwargs
) -> Dict[str, Any]:
    """Create or update privacy policy."""
    key = f"{PRIVACY_POLICY_KEY}_{language}"
    result = await db.execute(
        select(SystemSettings).where(SystemSettings.key == key)
    )
    existing = result.scalar_one_or_none()
    
    if existing:
        existing.value = content
        existing.updated_at = datetime.utcnow()
        await db.commit()
        await db.refresh(existing)
        return {
            'id': existing.id,
            'language': language,
            'content': content,
            'updated_at': existing.updated_at
        }
    
    setting = SystemSettings(key=key, value=content)
    db.add(setting)
    await db.commit()
    await db.refresh(setting)
    return {
        'id': setting.id,
        'language': language,
        'content': content,
        'updated_at': setting.updated_at
    }
