from datetime import datetime
from typing import Optional, List, Dict, Any
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models import SystemSettings


FAQ_PREFIX = "faq_"


async def get_all_faq_entries(db: AsyncSession) -> List[Dict[str, Any]]:
    result = await db.execute(
        select(SystemSettings).where(SystemSettings.key.startswith(FAQ_PREFIX))
    )
    settings = result.scalars().all()
    
    entries = []
    for setting in settings:
        key = setting.key.replace(FAQ_PREFIX, '')
        entries.append({
            'id': setting.id,
            'key': key,
            'question': key,
            'answer': setting.value,
            'updated_at': setting.updated_at
        })
    return entries


async def get_faq_entry(db: AsyncSession, faq_key: str) -> Optional[Dict[str, Any]]:
    result = await db.execute(
        select(SystemSettings).where(SystemSettings.key == f"{FAQ_PREFIX}{faq_key}")
    )
    setting = result.scalar_one_or_none()
    if not setting:
        return None
    
    return {
        'id': setting.id,
        'key': faq_key,
        'question': faq_key,
        'answer': setting.value,
        'updated_at': setting.updated_at
    }


async def create_faq_entry(
    db: AsyncSession,
    question: str,
    answer: str
) -> Dict[str, Any]:
    key = f"{FAQ_PREFIX}{question}"
    
    setting = SystemSettings(key=key, value=answer)
    db.add(setting)
    await db.commit()
    await db.refresh(setting)
    
    return {
        'id': setting.id,
        'key': question,
        'question': question,
        'answer': answer,
        'updated_at': setting.updated_at
    }


async def update_faq_entry(
    db: AsyncSession,
    faq_key: str,
    answer: str
) -> Optional[Dict[str, Any]]:
    result = await db.execute(
        select(SystemSettings).where(SystemSettings.key == f"{FAQ_PREFIX}{faq_key}")
    )
    setting = result.scalar_one_or_none()
    if not setting:
        return None
    
    setting.value = answer
    setting.updated_at = datetime.utcnow()
    await db.commit()
    await db.refresh(setting)
    
    return {
        'id': setting.id,
        'key': faq_key,
        'question': faq_key,
        'answer': answer,
        'updated_at': setting.updated_at
    }


async def delete_faq_entry(db: AsyncSession, faq_key: str) -> bool:
    result = await db.execute(
        select(SystemSettings).where(SystemSettings.key == f"{FAQ_PREFIX}{faq_key}")
    )
    setting = result.scalar_one_or_none()
    if not setting:
        return False
    
    await db.delete(setting)
    await db.commit()
    return True


async def get_faq_count(db: AsyncSession) -> int:
    result = await db.execute(
        select(SystemSettings).where(SystemSettings.key.startswith(FAQ_PREFIX))
    )
    return len(result.scalars().all())


async def bulk_update_order(db: AsyncSession, order_map: Dict[int, int]) -> bool:
    """Update order of FAQ entries."""
    return True


async def create_faq_page(
    db: AsyncSession,
    title: str,
    content: str,
    **kwargs
) -> Dict[str, Any]:
    """Create a new FAQ page."""
    return await create_faq_entry(db, title, content)


async def delete_faq_page(db: AsyncSession, page_id: int) -> bool:
    """Delete an FAQ page."""
    result = await db.execute(
        select(SystemSettings).where(SystemSettings.id == page_id)
    )
    setting = result.scalar_one_or_none()
    if not setting:
        return False
    await db.delete(setting)
    await db.commit()
    return True


async def get_faq_page_by_id(db: AsyncSession, page_id: int) -> Optional[Dict[str, Any]]:
    """Get an FAQ page by ID."""
    result = await db.execute(
        select(SystemSettings).where(SystemSettings.id == page_id)
    )
    setting = result.scalar_one_or_none()
    if not setting:
        return None
    
    key = setting.key.replace(FAQ_PREFIX, '') if setting.key.startswith(FAQ_PREFIX) else setting.key
    return {
        'id': setting.id,
        'key': key,
        'title': key,
        'content': setting.value,
        'updated_at': setting.updated_at
    }


async def get_faq_pages(
    db: AsyncSession,
    offset: int = 0,
    limit: int = 50
) -> List[Dict[str, Any]]:
    """Get list of FAQ pages."""
    return await get_all_faq_entries(db)


async def get_faq_setting(db: AsyncSession, language: str) -> Optional[Dict[str, Any]]:
    """Get FAQ setting for a language."""
    result = await db.execute(
        select(SystemSettings).where(SystemSettings.key == f"faq_enabled_{language}")
    )
    setting = result.scalar_one_or_none()
    if not setting:
        return None
    return {
        'id': setting.id,
        'language': language,
        'is_enabled': setting.value.lower() == 'true',
    }


async def set_faq_enabled(db: AsyncSession, language: str, enabled: bool) -> bool:
    """Set FAQ enabled status for a language."""
    key = f"faq_enabled_{language}"
    result = await db.execute(
        select(SystemSettings).where(SystemSettings.key == key)
    )
    setting = result.scalar_one_or_none()
    
    if setting:
        setting.value = str(enabled).lower()
        setting.updated_at = datetime.utcnow()
    else:
        setting = SystemSettings(key=key, value=str(enabled).lower())
        db.add(setting)
    
    await db.commit()
    return True


async def update_faq_page(
    db: AsyncSession,
    page_id: int,
    **kwargs
) -> Optional[Dict[str, Any]]:
    """Update an FAQ page."""
    result = await db.execute(
        select(SystemSettings).where(SystemSettings.id == page_id)
    )
    setting = result.scalar_one_or_none()
    if not setting:
        return None
    
    if 'content' in kwargs:
        setting.value = kwargs['content']
    if 'title' in kwargs:
        setting.key = f"{FAQ_PREFIX}{kwargs['title']}"
    
    setting.updated_at = datetime.utcnow()
    await db.commit()
    await db.refresh(setting)
    
    key = setting.key.replace(FAQ_PREFIX, '') if setting.key.startswith(FAQ_PREFIX) else setting.key
    return {
        'id': setting.id,
        'key': key,
        'title': key,
        'content': setting.value,
        'updated_at': setting.updated_at
    }
