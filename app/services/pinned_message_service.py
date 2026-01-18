import logging
from datetime import datetime
from typing import Optional, Tuple, Any

from aiogram import Bot
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

logger = logging.getLogger(__name__)


async def broadcast_pinned_message(
    bot: Bot,
    db: AsyncSession,
    pinned_message: Any,
) -> Tuple[int, int]:
    sent_count = 0
    failed_count = 0
    return sent_count, failed_count


async def get_active_pinned_message(db: AsyncSession) -> Optional[Any]:
    try:
        from app.database.models import PinnedMessage
        result = await db.execute(
            select(PinnedMessage)
            .where(PinnedMessage.is_active == True)
            .order_by(PinnedMessage.created_at.desc())
            .limit(1)
        )
        return result.scalar_one_or_none()
    except Exception:
        return None


async def set_active_pinned_message(
    db: AsyncSession,
    content: str,
    created_by: int,
    media_type: Optional[str] = None,
    media_file_id: Optional[str] = None,
) -> Any:
    try:
        from app.database.models import PinnedMessage

        existing = await get_active_pinned_message(db)
        if existing:
            existing.is_active = False
            existing.updated_at = datetime.utcnow()

        pinned_message = PinnedMessage(
            content=content,
            created_by=created_by,
            media_type=media_type,
            media_file_id=media_file_id,
            is_active=True,
            send_before_menu=True,
            send_on_every_start=True,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        db.add(pinned_message)
        await db.commit()
        await db.refresh(pinned_message)
        return pinned_message
    except Exception as e:
        logger.error("Error setting pinned message: %s", e)
        raise ValueError(str(e))


async def unpin_active_pinned_message(
    bot: Bot,
    db: AsyncSession,
) -> Tuple[int, int, bool]:
    unpinned_count = 0
    failed_count = 0
    deleted = False

    pinned_message = await get_active_pinned_message(db)
    if pinned_message:
        pinned_message.is_active = False
        pinned_message.updated_at = datetime.utcnow()
        await db.commit()
        deleted = True

    return unpinned_count, failed_count, deleted
