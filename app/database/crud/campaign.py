from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession


async def get_campaign_by_start_parameter(db: AsyncSession, param: str) -> Optional[dict]:
    return None
