from datetime import datetime
from typing import Optional, Dict, Any
from sqlalchemy import select, func, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models import ServiceRule


async def get_current_rules_content(db: AsyncSession) -> Optional[str]:
    result = await db.execute(
        select(ServiceRule)
        .where(ServiceRule.rule_type == 'content')
        .where(ServiceRule.is_active == True)
        .order_by(ServiceRule.created_at.desc())
        .limit(1)
    )
    rule = result.scalar_one_or_none()
    return rule.rule_value if rule else None


async def create_or_update_rules(
    db: AsyncSession,
    content: str,
    rule_type: str = 'content'
) -> ServiceRule:
    result = await db.execute(
        select(ServiceRule)
        .where(ServiceRule.rule_type == rule_type)
        .limit(1)
    )
    existing = result.scalar_one_or_none()
    
    if existing:
        existing.rule_value = content
        existing.updated_at = datetime.utcnow()
        await db.commit()
        await db.refresh(existing)
        return existing
    
    rule = ServiceRule(
        rule_type=rule_type,
        rule_value=content,
        is_active=True
    )
    db.add(rule)
    await db.commit()
    await db.refresh(rule)
    return rule


async def clear_all_rules(db: AsyncSession) -> int:
    result = await db.execute(
        select(func.count(ServiceRule.id))
    )
    count = result.scalar() or 0
    
    await db.execute(delete(ServiceRule))
    await db.commit()
    return count


async def get_rules_statistics(db: AsyncSession) -> Dict[str, Any]:
    total_result = await db.execute(
        select(func.count(ServiceRule.id))
    )
    total = total_result.scalar() or 0
    
    active_result = await db.execute(
        select(func.count(ServiceRule.id)).where(ServiceRule.is_active == True)
    )
    active = active_result.scalar() or 0
    
    return {
        'total_rules': total,
        'active_rules': active,
        'inactive_rules': total - active
    }


async def get_rule_by_id(db: AsyncSession, rule_id: int) -> Optional[ServiceRule]:
    result = await db.execute(
        select(ServiceRule).where(ServiceRule.id == rule_id)
    )
    return result.scalar_one_or_none()


async def get_all_rules(db: AsyncSession) -> list[ServiceRule]:
    result = await db.execute(
        select(ServiceRule).order_by(ServiceRule.created_at.desc())
    )
    return result.scalars().all()


async def create_rule(
    db: AsyncSession,
    rule_type: str,
    rule_value: Optional[str] = None,
    description: Optional[str] = None,
    is_active: bool = True
) -> ServiceRule:
    rule = ServiceRule(
        rule_type=rule_type,
        rule_value=rule_value,
        description=description,
        is_active=is_active
    )
    db.add(rule)
    await db.commit()
    await db.refresh(rule)
    return rule


async def update_rule(
    db: AsyncSession,
    rule_id: int,
    **kwargs
) -> Optional[ServiceRule]:
    rule = await get_rule_by_id(db, rule_id)
    if not rule:
        return None
    
    for key, value in kwargs.items():
        if hasattr(rule, key):
            setattr(rule, key, value)
    
    rule.updated_at = datetime.utcnow()
    await db.commit()
    await db.refresh(rule)
    return rule


async def delete_rule(db: AsyncSession, rule_id: int) -> bool:
    rule = await get_rule_by_id(db, rule_id)
    if not rule:
        return False
    await db.delete(rule)
    await db.commit()
    return True
