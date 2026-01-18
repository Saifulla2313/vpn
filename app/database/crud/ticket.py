from datetime import datetime
from typing import Optional, List, Dict, Any
from sqlalchemy import select, func, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.database.models import Ticket, TicketMessage, TicketStatus


class TicketCRUD:
    @staticmethod
    async def get_ticket_by_id(
        db: AsyncSession,
        ticket_id: int,
        load_messages: bool = False,
        load_user: bool = False
    ) -> Optional[Ticket]:
        query = select(Ticket).where(Ticket.id == ticket_id)
        if load_messages:
            query = query.options(selectinload(Ticket.messages))
        if load_user:
            query = query.options(selectinload(Ticket.user))
        result = await db.execute(query)
        return result.scalar_one_or_none()

    @staticmethod
    async def get_tickets_by_user_id(
        db: AsyncSession,
        user_id: int,
        limit: int = 10,
        offset: int = 0
    ) -> List[Ticket]:
        result = await db.execute(
            select(Ticket)
            .where(Ticket.user_id == user_id)
            .order_by(Ticket.created_at.desc())
            .offset(offset)
            .limit(limit)
        )
        return result.scalars().all()

    @staticmethod
    async def get_tickets_by_statuses(
        db: AsyncSession,
        statuses: List[str],
        limit: int = 10,
        offset: int = 0
    ) -> List[Ticket]:
        result = await db.execute(
            select(Ticket)
            .options(selectinload(Ticket.user))
            .where(Ticket.status.in_(statuses))
            .order_by(Ticket.updated_at.desc())
            .offset(offset)
            .limit(limit)
        )
        return result.scalars().all()

    @staticmethod
    async def count_tickets_by_statuses(
        db: AsyncSession,
        statuses: List[str]
    ) -> int:
        result = await db.execute(
            select(func.count(Ticket.id)).where(Ticket.status.in_(statuses))
        )
        return result.scalar() or 0

    @staticmethod
    async def create_ticket(
        db: AsyncSession,
        user_id: int,
        title: str,
        initial_message: Optional[str] = None
    ) -> Ticket:
        ticket = Ticket(
            user_id=user_id,
            title=title,
            status=TicketStatus.OPEN.value
        )
        db.add(ticket)
        await db.commit()
        await db.refresh(ticket)
        
        if initial_message:
            message = TicketMessage(
                ticket_id=ticket.id,
                user_id=user_id,
                message_text=initial_message,
                is_from_admin=False
            )
            db.add(message)
            await db.commit()
        
        return ticket

    @staticmethod
    async def update_ticket_status(
        db: AsyncSession,
        ticket_id: int,
        status: str
    ) -> Optional[Ticket]:
        ticket = await TicketCRUD.get_ticket_by_id(db, ticket_id)
        if not ticket:
            return None
        
        ticket.status = status
        ticket.updated_at = datetime.utcnow()
        if status == TicketStatus.CLOSED.value:
            ticket.closed_at = datetime.utcnow()
        
        await db.commit()
        await db.refresh(ticket)
        return ticket

    @staticmethod
    async def close_ticket(db: AsyncSession, ticket_id: int) -> Optional[Ticket]:
        return await TicketCRUD.update_ticket_status(db, ticket_id, TicketStatus.CLOSED.value)

    @staticmethod
    async def delete_ticket(db: AsyncSession, ticket_id: int) -> bool:
        ticket = await TicketCRUD.get_ticket_by_id(db, ticket_id)
        if not ticket:
            return False
        await db.delete(ticket)
        await db.commit()
        return True

    @staticmethod
    async def get_open_tickets_count(db: AsyncSession) -> int:
        return await TicketCRUD.count_tickets_by_statuses(
            db, [TicketStatus.OPEN.value, TicketStatus.PENDING.value]
        )

    @staticmethod
    async def block_user_reply(
        db: AsyncSession,
        ticket_id: int,
        permanent: bool = False,
        until: Optional[datetime] = None
    ) -> Optional[Ticket]:
        ticket = await TicketCRUD.get_ticket_by_id(db, ticket_id)
        if not ticket:
            return None
        
        ticket.is_user_reply_blocked = True
        ticket.user_reply_block_permanent = permanent
        ticket.user_reply_block_until = until
        ticket.updated_at = datetime.utcnow()
        
        await db.commit()
        await db.refresh(ticket)
        return ticket

    @staticmethod
    async def unblock_user_reply(db: AsyncSession, ticket_id: int) -> Optional[Ticket]:
        ticket = await TicketCRUD.get_ticket_by_id(db, ticket_id)
        if not ticket:
            return None
        
        ticket.is_user_reply_blocked = False
        ticket.user_reply_block_permanent = False
        ticket.user_reply_block_until = None
        ticket.updated_at = datetime.utcnow()
        
        await db.commit()
        await db.refresh(ticket)
        return ticket


class TicketMessageCRUD:
    @staticmethod
    async def get_message_by_id(
        db: AsyncSession,
        message_id: int
    ) -> Optional[TicketMessage]:
        result = await db.execute(
            select(TicketMessage).where(TicketMessage.id == message_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def get_ticket_messages(
        db: AsyncSession,
        ticket_id: int,
        limit: int = 100,
        offset: int = 0
    ) -> List[TicketMessage]:
        result = await db.execute(
            select(TicketMessage)
            .where(TicketMessage.ticket_id == ticket_id)
            .order_by(TicketMessage.created_at.asc())
            .offset(offset)
            .limit(limit)
        )
        return result.scalars().all()

    @staticmethod
    async def create_message(
        db: AsyncSession,
        ticket_id: int,
        user_id: int,
        message_text: Optional[str] = None,
        is_from_admin: bool = False,
        has_media: bool = False,
        media_type: Optional[str] = None,
        media_file_id: Optional[str] = None,
        media_caption: Optional[str] = None
    ) -> TicketMessage:
        message = TicketMessage(
            ticket_id=ticket_id,
            user_id=user_id,
            message_text=message_text,
            is_from_admin=is_from_admin,
            has_media=has_media,
            media_type=media_type,
            media_file_id=media_file_id,
            media_caption=media_caption
        )
        db.add(message)
        
        ticket = await TicketCRUD.get_ticket_by_id(db, ticket_id)
        if ticket:
            ticket.updated_at = datetime.utcnow()
            if is_from_admin:
                ticket.status = TicketStatus.ANSWERED.value
            else:
                if ticket.status == TicketStatus.ANSWERED.value:
                    ticket.status = TicketStatus.OPEN.value
        
        await db.commit()
        await db.refresh(message)
        return message

    @staticmethod
    async def count_ticket_messages(db: AsyncSession, ticket_id: int) -> int:
        result = await db.execute(
            select(func.count(TicketMessage.id))
            .where(TicketMessage.ticket_id == ticket_id)
        )
        return result.scalar() or 0

    @staticmethod
    async def delete_message(db: AsyncSession, message_id: int) -> bool:
        message = await TicketMessageCRUD.get_message_by_id(db, message_id)
        if not message:
            return False
        await db.delete(message)
        await db.commit()
        return True
