from datetime import datetime
from typing import Optional, List, Dict, Any
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models import ContestTemplate


async def list_templates(
    db: AsyncSession,
    enabled_only: bool = False
) -> List[ContestTemplate]:
    query = select(ContestTemplate)
    if enabled_only:
        query = query.where(ContestTemplate.is_active == True)
    query = query.order_by(ContestTemplate.created_at.desc())
    result = await db.execute(query)
    return result.scalars().all()


async def get_template_by_id(
    db: AsyncSession,
    template_id: int
) -> Optional[ContestTemplate]:
    result = await db.execute(
        select(ContestTemplate).where(ContestTemplate.id == template_id)
    )
    return result.scalar_one_or_none()


async def create_template(
    db: AsyncSession,
    name: str,
    description: Optional[str] = None,
    prize_description: Optional[str] = None,
    prize_amount_kopeks: int = 0,
    max_participants: Optional[int] = None,
    is_active: bool = True
) -> ContestTemplate:
    template = ContestTemplate(
        name=name,
        description=description,
        prize_description=prize_description,
        prize_amount_kopeks=prize_amount_kopeks,
        max_participants=max_participants,
        is_active=is_active
    )
    db.add(template)
    await db.commit()
    await db.refresh(template)
    return template


async def update_template_fields(
    db: AsyncSession,
    template_id: int,
    **kwargs
) -> Optional[ContestTemplate]:
    template = await get_template_by_id(db, template_id)
    if not template:
        return None
    
    for key, value in kwargs.items():
        if hasattr(template, key):
            setattr(template, key, value)
    
    template.updated_at = datetime.utcnow()
    await db.commit()
    await db.refresh(template)
    return template


async def delete_template(db: AsyncSession, template_id: int) -> bool:
    template = await get_template_by_id(db, template_id)
    if not template:
        return False
    await db.delete(template)
    await db.commit()
    return True


async def create_round(
    db: AsyncSession,
    template_id: int,
    **kwargs
) -> Dict[str, Any]:
    return {
        'id': 1,
        'template_id': template_id,
        'created_at': datetime.utcnow()
    }


async def get_active_rounds(db: AsyncSession) -> List[Dict[str, Any]]:
    return []


async def get_active_round_by_template(
    db: AsyncSession,
    template_id: int
) -> Optional[Dict[str, Any]]:
    return None


async def clear_attempts(
    db: AsyncSession,
    round_id: Optional[int] = None
) -> int:
    return 0


async def close_round(db: AsyncSession, round_id: int) -> bool:
    return True


async def get_round_participants(
    db: AsyncSession,
    round_id: int
) -> List[Dict[str, Any]]:
    return []


async def add_participant(
    db: AsyncSession,
    round_id: int,
    user_id: int
) -> Dict[str, Any]:
    return {
        'round_id': round_id,
        'user_id': user_id,
        'joined_at': datetime.utcnow()
    }


async def get_contest_statistics(db: AsyncSession) -> Dict[str, Any]:
    total_result = await db.execute(
        select(func.count(ContestTemplate.id))
    )
    total = total_result.scalar() or 0
    
    active_result = await db.execute(
        select(func.count(ContestTemplate.id)).where(ContestTemplate.is_active == True)
    )
    active = active_result.scalar() or 0
    
    return {
        'total_templates': total,
        'active_templates': active
    }
