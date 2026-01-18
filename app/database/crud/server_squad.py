from datetime import datetime
from typing import Optional, List, Dict, Any
from sqlalchemy import select, func, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.database.models import ServerSquad, PromoGroup, server_squad_promo_groups


async def get_all_server_squads(db: AsyncSession, include_inactive: bool = True) -> List[ServerSquad]:
    query = select(ServerSquad).options(selectinload(ServerSquad.promo_groups))
    if not include_inactive:
        query = query.where(ServerSquad.is_available == True)
    query = query.order_by(ServerSquad.sort_order, ServerSquad.id)
    result = await db.execute(query)
    return result.scalars().all()


async def get_available_server_squads(db: AsyncSession) -> List[ServerSquad]:
    return await get_all_server_squads(db, include_inactive=False)


async def get_server_squad_by_id(db: AsyncSession, squad_id: int) -> Optional[ServerSquad]:
    result = await db.execute(
        select(ServerSquad)
        .options(selectinload(ServerSquad.promo_groups))
        .where(ServerSquad.id == squad_id)
    )
    return result.scalar_one_or_none()


async def get_server_squad_by_uuid(db: AsyncSession, squad_uuid: str) -> Optional[ServerSquad]:
    result = await db.execute(
        select(ServerSquad)
        .options(selectinload(ServerSquad.promo_groups))
        .where(ServerSquad.squad_uuid == squad_uuid)
    )
    return result.scalar_one_or_none()


async def create_server_squad(
    db: AsyncSession,
    squad_uuid: str,
    display_name: str,
    original_name: Optional[str] = None,
    country_code: Optional[str] = None,
    price_kopeks: int = 0,
    description: Optional[str] = None,
    is_available: bool = True,
    is_trial_eligible: bool = False,
    sort_order: int = 0,
    max_users: Optional[int] = None
) -> ServerSquad:
    squad = ServerSquad(
        squad_uuid=squad_uuid,
        display_name=display_name,
        original_name=original_name,
        country_code=country_code,
        price_kopeks=price_kopeks,
        description=description,
        is_available=is_available,
        is_trial_eligible=is_trial_eligible,
        sort_order=sort_order,
        max_users=max_users
    )
    db.add(squad)
    await db.commit()
    await db.refresh(squad)
    return squad


async def update_server_squad(
    db: AsyncSession,
    squad_id: int,
    **kwargs
) -> Optional[ServerSquad]:
    squad = await get_server_squad_by_id(db, squad_id)
    if not squad:
        return None
    
    for key, value in kwargs.items():
        if hasattr(squad, key):
            setattr(squad, key, value)
    
    squad.updated_at = datetime.utcnow()
    await db.commit()
    await db.refresh(squad)
    return squad


async def delete_server_squad(db: AsyncSession, squad_id: int) -> bool:
    squad = await get_server_squad_by_id(db, squad_id)
    if not squad:
        return False
    await db.delete(squad)
    await db.commit()
    return True


async def sync_with_remnawave(db: AsyncSession, squads_data: List[Dict[str, Any]]) -> Dict[str, int]:
    created = 0
    updated = 0
    
    for data in squads_data:
        squad_uuid = data.get('uuid') or data.get('squad_uuid')
        if not squad_uuid:
            continue
        
        existing = await get_server_squad_by_uuid(db, squad_uuid)
        if existing:
            for key, value in data.items():
                if hasattr(existing, key) and key != 'id':
                    setattr(existing, key, value)
            existing.updated_at = datetime.utcnow()
            updated += 1
        else:
            squad = ServerSquad(
                squad_uuid=squad_uuid,
                display_name=data.get('display_name', data.get('name', squad_uuid)),
                original_name=data.get('original_name', data.get('name')),
                country_code=data.get('country_code'),
                is_available=data.get('is_available', True)
            )
            db.add(squad)
            created += 1
    
    await db.commit()
    return {'created': created, 'updated': updated}


async def get_server_statistics(db: AsyncSession) -> Dict[str, Any]:
    total_result = await db.execute(select(func.count(ServerSquad.id)))
    total = total_result.scalar() or 0
    
    available_result = await db.execute(
        select(func.count(ServerSquad.id)).where(ServerSquad.is_available == True)
    )
    available = available_result.scalar() or 0
    
    trial_result = await db.execute(
        select(func.count(ServerSquad.id)).where(ServerSquad.is_trial_eligible == True)
    )
    trial_eligible = trial_result.scalar() or 0
    
    return {
        'total': total,
        'available': available,
        'unavailable': total - available,
        'trial_eligible': trial_eligible
    }


async def update_server_squad_promo_groups(
    db: AsyncSession,
    squad_id: int,
    promo_group_ids: List[int]
) -> Optional[ServerSquad]:
    squad = await get_server_squad_by_id(db, squad_id)
    if not squad:
        return None
    
    await db.execute(
        delete(server_squad_promo_groups).where(
            server_squad_promo_groups.c.server_squad_id == squad_id
        )
    )
    
    for pg_id in promo_group_ids:
        await db.execute(
            server_squad_promo_groups.insert().values(
                server_squad_id=squad_id,
                promo_group_id=pg_id
            )
        )
    
    await db.commit()
    await db.refresh(squad)
    return squad


async def get_server_connected_users(db: AsyncSession, squad_id: int) -> int:
    squad = await get_server_squad_by_id(db, squad_id)
    return squad.current_users if squad else 0


async def sync_server_user_counts(db: AsyncSession, counts: Dict[str, int]) -> None:
    for squad_uuid, count in counts.items():
        squad = await get_server_squad_by_uuid(db, squad_uuid)
        if squad:
            squad.current_users = count
            squad.updated_at = datetime.utcnow()
    await db.commit()


async def get_random_trial_squad_uuid(db: AsyncSession) -> Optional[str]:
    result = await db.execute(
        select(ServerSquad.squad_uuid)
        .where(ServerSquad.is_trial_eligible == True)
        .where(ServerSquad.is_available == True)
        .order_by(func.random())
        .limit(1)
    )
    squad_uuid = result.scalar_one_or_none()
    return squad_uuid


async def add_user_to_servers(
    db: AsyncSession,
    user_id: int,
    server_uuids: List[str]
) -> bool:
    """Add user to specified servers."""
    for squad_uuid in server_uuids:
        squad = await get_server_squad_by_uuid(db, squad_uuid)
        if squad:
            squad.current_users = (squad.current_users or 0) + 1
            squad.updated_at = datetime.utcnow()
    await db.commit()
    return True


async def remove_user_from_servers(
    db: AsyncSession,
    user_id: int,
    server_uuids: List[str]
) -> bool:
    """Remove user from specified servers."""
    for squad_uuid in server_uuids:
        squad = await get_server_squad_by_uuid(db, squad_uuid)
        if squad and squad.current_users > 0:
            squad.current_users = squad.current_users - 1
            squad.updated_at = datetime.utcnow()
    await db.commit()
    return True


async def count_active_users_for_squad(db: AsyncSession, squad_uuid: str) -> int:
    """Count active users for a specific squad."""
    squad = await get_server_squad_by_uuid(db, squad_uuid)
    return squad.current_users if squad else 0


async def get_server_ids_by_uuids(
    db: AsyncSession,
    server_uuids: List[str]
) -> List[int]:
    """Get server IDs by their UUIDs."""
    result = await db.execute(
        select(ServerSquad.id)
        .where(ServerSquad.squad_uuid.in_(server_uuids))
    )
    return [row[0] for row in result.all()]
