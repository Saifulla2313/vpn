from datetime import datetime
from typing import Optional, List, Dict, Any
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models import UserMessage


async def get_all_user_messages(
    db: AsyncSession,
    limit: int = 50,
    offset: int = 0
) -> List[UserMessage]:
    result = await db.execute(
        select(UserMessage)
        .order_by(UserMessage.created_at.desc())
        .offset(offset)
        .limit(limit)
    )
    return result.scalars().all()


async def get_user_message_by_id(db: AsyncSession, message_id: int) -> Optional[UserMessage]:
    result = await db.execute(
        select(UserMessage).where(UserMessage.id == message_id)
    )
    return result.scalar_one_or_none()


async def get_user_messages_by_user_id(
    db: AsyncSession,
    user_id: int,
    limit: int = 50
) -> List[UserMessage]:
    result = await db.execute(
        select(UserMessage)
        .where(UserMessage.user_id == user_id)
        .order_by(UserMessage.created_at.desc())
        .limit(limit)
    )
    return result.scalars().all()


async def create_user_message(
    db: AsyncSession,
    user_id: int,
    message_text: Optional[str] = None,
    is_from_admin: bool = False,
    admin_id: Optional[int] = None,
    message_id: Optional[int] = None,
    has_media: bool = False,
    media_type: Optional[str] = None,
    media_file_id: Optional[str] = None
) -> UserMessage:
    message = UserMessage(
        user_id=user_id,
        message_text=message_text,
        is_from_admin=is_from_admin,
        admin_id=admin_id,
        message_id=message_id,
        has_media=has_media,
        media_type=media_type,
        media_file_id=media_file_id
    )
    db.add(message)
    await db.commit()
    await db.refresh(message)
    return message


async def update_user_message(
    db: AsyncSession,
    message_id: int,
    **kwargs
) -> Optional[UserMessage]:
    message = await get_user_message_by_id(db, message_id)
    if not message:
        return None
    
    for key, value in kwargs.items():
        if hasattr(message, key):
            setattr(message, key, value)
    
    await db.commit()
    await db.refresh(message)
    return message


async def delete_user_message(db: AsyncSession, message_id: int) -> bool:
    message = await get_user_message_by_id(db, message_id)
    if not message:
        return False
    await db.delete(message)
    await db.commit()
    return True


async def toggle_user_message_status(db: AsyncSession, message_id: int) -> Optional[UserMessage]:
    message = await get_user_message_by_id(db, message_id)
    if not message:
        return None
    
    await db.commit()
    await db.refresh(message)
    return message


async def get_user_messages_stats(db: AsyncSession) -> Dict[str, Any]:
    total_result = await db.execute(
        select(func.count(UserMessage.id))
    )
    total = total_result.scalar() or 0
    
    from_admin_result = await db.execute(
        select(func.count(UserMessage.id)).where(UserMessage.is_from_admin == True)
    )
    from_admin = from_admin_result.scalar() or 0
    
    with_media_result = await db.execute(
        select(func.count(UserMessage.id)).where(UserMessage.has_media == True)
    )
    with_media = with_media_result.scalar() or 0
    
    return {
        'total_messages': total,
        'from_admin': from_admin,
        'from_users': total - from_admin,
        'with_media': with_media
    }
