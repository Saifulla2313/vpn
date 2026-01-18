from datetime import datetime
from typing import Optional, List, Dict, Any
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models import WelcomeText


async def get_active_welcome_text(db: AsyncSession) -> Optional[WelcomeText]:
    result = await db.execute(
        select(WelcomeText)
        .where(WelcomeText.is_active == True)
        .where(WelcomeText.is_enabled == True)
        .order_by(WelcomeText.created_at.desc())
        .limit(1)
    )
    return result.scalar_one_or_none()


async def get_current_welcome_text_or_default(db: AsyncSession) -> str:
    welcome = await get_active_welcome_text(db)
    if welcome:
        return welcome.text
    return "Добро пожаловать!"


async def set_welcome_text(
    db: AsyncSession,
    text: str,
    created_by: Optional[int] = None
) -> WelcomeText:
    result = await db.execute(
        select(WelcomeText).where(WelcomeText.is_active == True).limit(1)
    )
    existing = result.scalar_one_or_none()
    
    if existing:
        existing.text = text
        existing.updated_at = datetime.utcnow()
        if created_by:
            existing.created_by = created_by
        await db.commit()
        await db.refresh(existing)
        return existing
    
    welcome = WelcomeText(
        text=text,
        is_active=True,
        is_enabled=True,
        created_by=created_by
    )
    db.add(welcome)
    await db.commit()
    await db.refresh(welcome)
    return welcome


async def get_available_placeholders() -> Dict[str, str]:
    return {
        '{username}': 'Имя пользователя',
        '{first_name}': 'Имя',
        '{last_name}': 'Фамилия',
        '{user_id}': 'ID пользователя',
        '{telegram_id}': 'Telegram ID',
        '{balance}': 'Баланс пользователя',
        '{referral_link}': 'Реферальная ссылка'
    }


async def get_current_welcome_text_settings(db: AsyncSession) -> Dict[str, Any]:
    welcome = await get_active_welcome_text(db)
    if not welcome:
        return {
            'text': None,
            'is_enabled': False,
            'created_at': None,
            'updated_at': None
        }
    
    return {
        'id': welcome.id,
        'text': welcome.text,
        'is_active': welcome.is_active,
        'is_enabled': welcome.is_enabled,
        'created_by': welcome.created_by,
        'created_at': welcome.created_at,
        'updated_at': welcome.updated_at
    }


async def toggle_welcome_text_status(db: AsyncSession) -> bool:
    welcome = await get_active_welcome_text(db)
    if not welcome:
        return False
    
    welcome.is_enabled = not welcome.is_enabled
    welcome.updated_at = datetime.utcnow()
    await db.commit()
    return welcome.is_enabled


async def get_welcome_text_for_user(
    db: AsyncSession,
    user_data: Dict[str, Any]
) -> str:
    text = await get_current_welcome_text_or_default(db)
    
    for key, value in user_data.items():
        placeholder = f'{{{key}}}'
        if placeholder in text:
            text = text.replace(placeholder, str(value))
    
    return text


async def get_all_welcome_texts(db: AsyncSession) -> List[WelcomeText]:
    result = await db.execute(
        select(WelcomeText).order_by(WelcomeText.created_at.desc())
    )
    return result.scalars().all()


async def delete_welcome_text(db: AsyncSession, welcome_id: int) -> bool:
    result = await db.execute(
        select(WelcomeText).where(WelcomeText.id == welcome_id)
    )
    welcome = result.scalar_one_or_none()
    if not welcome:
        return False
    await db.delete(welcome)
    await db.commit()
    return True
