from datetime import datetime
from typing import Optional, List
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models import Transaction, TransactionType, TransactionStatus


async def create_transaction(
    db: AsyncSession,
    user_id: int,
    transaction_type: TransactionType,
    amount: float,
    description: str = "",
    payment_id: str = None,
    payment_method: str = None,
    currency: str = "RUB"
) -> Transaction:
    transaction = Transaction(
        user_id=user_id,
        type=transaction_type,
        amount=amount,
        description=description,
        payment_id=payment_id,
        payment_method=payment_method,
        currency=currency,
        status=TransactionStatus.PENDING
    )
    db.add(transaction)
    await db.commit()
    await db.refresh(transaction)
    return transaction


async def complete_transaction(db: AsyncSession, transaction_id: int) -> Optional[Transaction]:
    result = await db.execute(select(Transaction).where(Transaction.id == transaction_id))
    transaction = result.scalar_one_or_none()
    if transaction:
        transaction.status = TransactionStatus.COMPLETED
        transaction.completed_at = datetime.utcnow()
        await db.commit()
        await db.refresh(transaction)
    return transaction


async def get_transaction_by_payment_id(db: AsyncSession, payment_id: str) -> Optional[Transaction]:
    result = await db.execute(select(Transaction).where(Transaction.payment_id == payment_id))
    return result.scalar_one_or_none()


async def get_user_transactions(
    db: AsyncSession,
    user_id: int,
    limit: int = 10
) -> List[Transaction]:
    result = await db.execute(
        select(Transaction)
        .where(Transaction.user_id == user_id)
        .order_by(desc(Transaction.created_at))
        .limit(limit)
    )
    return result.scalars().all()
