from datetime import datetime
from typing import Optional, List, Dict, Any
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models import Poll, PollQuestion, PollOption, PollResponse, PollAnswer


async def list_polls(
    db: AsyncSession,
    active_only: bool = False,
    limit: int = 100,
    offset: int = 0
) -> List[Poll]:
    query = select(Poll)
    if active_only:
        query = query.where(Poll.is_active == True)
    query = query.order_by(Poll.created_at.desc()).offset(offset).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


async def get_poll_by_id(db: AsyncSession, poll_id: int) -> Optional[Poll]:
    result = await db.execute(select(Poll).where(Poll.id == poll_id))
    return result.scalar_one_or_none()


async def create_poll(
    db: AsyncSession,
    title: str,
    description: Optional[str] = None,
    reward_enabled: bool = False,
    reward_amount_kopeks: int = 0,
    is_active: bool = True
) -> Poll:
    poll = Poll(
        title=title,
        description=description,
        reward_enabled=reward_enabled,
        reward_amount_kopeks=reward_amount_kopeks,
        is_active=is_active
    )
    db.add(poll)
    await db.commit()
    await db.refresh(poll)
    return poll


async def update_poll(
    db: AsyncSession,
    poll_id: int,
    **kwargs
) -> Optional[Poll]:
    poll = await get_poll_by_id(db, poll_id)
    if not poll:
        return None
    
    for key, value in kwargs.items():
        if hasattr(poll, key):
            setattr(poll, key, value)
    
    poll.updated_at = datetime.utcnow()
    await db.commit()
    await db.refresh(poll)
    return poll


async def delete_poll(db: AsyncSession, poll_id: int) -> bool:
    poll = await get_poll_by_id(db, poll_id)
    if not poll:
        return False
    await db.delete(poll)
    await db.commit()
    return True


async def get_poll_statistics(db: AsyncSession, poll_id: int) -> Dict[str, Any]:
    responses_result = await db.execute(
        select(func.count(PollResponse.id)).where(PollResponse.poll_id == poll_id)
    )
    total_responses = responses_result.scalar() or 0
    
    completed_result = await db.execute(
        select(func.count(PollResponse.id)).where(
            PollResponse.poll_id == poll_id,
            PollResponse.completed_at.isnot(None)
        )
    )
    completed_responses = completed_result.scalar() or 0
    
    return {
        'poll_id': poll_id,
        'total_responses': total_responses,
        'completed_responses': completed_responses,
        'completion_rate': (completed_responses / total_responses * 100) if total_responses > 0 else 0
    }


async def create_poll_question(
    db: AsyncSession,
    poll_id: int,
    text: str,
    order: int = 0
) -> PollQuestion:
    question = PollQuestion(
        poll_id=poll_id,
        text=text,
        order=order
    )
    db.add(question)
    await db.commit()
    await db.refresh(question)
    return question


async def create_poll_option(
    db: AsyncSession,
    question_id: int,
    text: str,
    order: int = 0
) -> PollOption:
    option = PollOption(
        question_id=question_id,
        text=text,
        order=order
    )
    db.add(option)
    await db.commit()
    await db.refresh(option)
    return option


async def get_poll_questions(db: AsyncSession, poll_id: int) -> List[PollQuestion]:
    result = await db.execute(
        select(PollQuestion)
        .where(PollQuestion.poll_id == poll_id)
        .order_by(PollQuestion.order)
    )
    return result.scalars().all()


async def get_question_options(db: AsyncSession, question_id: int) -> List[PollOption]:
    result = await db.execute(
        select(PollOption)
        .where(PollOption.question_id == question_id)
        .order_by(PollOption.order)
    )
    return result.scalars().all()


async def create_poll_response(
    db: AsyncSession,
    poll_id: int,
    user_id: int
) -> PollResponse:
    response = PollResponse(
        poll_id=poll_id,
        user_id=user_id,
        started_at=datetime.utcnow()
    )
    db.add(response)
    await db.commit()
    await db.refresh(response)
    return response


async def complete_poll_response(
    db: AsyncSession,
    response_id: int,
    reward_given: bool = False,
    reward_amount_kopeks: int = 0
) -> Optional[PollResponse]:
    result = await db.execute(
        select(PollResponse).where(PollResponse.id == response_id)
    )
    response = result.scalar_one_or_none()
    if not response:
        return None
    
    response.completed_at = datetime.utcnow()
    response.reward_given = reward_given
    response.reward_amount_kopeks = reward_amount_kopeks
    
    await db.commit()
    await db.refresh(response)
    return response
