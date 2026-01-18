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


async def get_transaction_by_id(db: AsyncSession, transaction_id: int) -> Optional[Transaction]:
    """Get transaction by ID."""
    result = await db.execute(select(Transaction).where(Transaction.id == transaction_id))
    return result.scalar_one_or_none()


async def get_transaction_by_external_id(
    db: AsyncSession,
    external_id: str,
    payment_method: str = None
) -> Optional[Transaction]:
    """Get transaction by external payment ID."""
    query = select(Transaction).where(Transaction.payment_id == external_id)
    if payment_method:
        query = query.where(Transaction.payment_method == payment_method)
    result = await db.execute(query)
    return result.scalar_one_or_none()


async def get_transactions_statistics(db: AsyncSession) -> dict:
    """Get transaction statistics."""
    from sqlalchemy import func
    
    total_result = await db.execute(
        select(func.count(Transaction.id))
    )
    total = total_result.scalar() or 0
    
    completed_result = await db.execute(
        select(func.count(Transaction.id)).where(
            Transaction.status == TransactionStatus.COMPLETED
        )
    )
    completed = completed_result.scalar() or 0
    
    total_amount_result = await db.execute(
        select(func.sum(Transaction.amount)).where(
            Transaction.status == TransactionStatus.COMPLETED
        )
    )
    total_amount = total_amount_result.scalar() or 0
    
    return {
        'total': total,
        'completed': completed,
        'pending': total - completed,
        'total_amount': total_amount
    }


async def get_revenue_by_period(
    db: AsyncSession,
    start_date: datetime = None,
    end_date: datetime = None
) -> float:
    """Get total revenue for a period."""
    from sqlalchemy import func
    
    query = select(func.sum(Transaction.amount)).where(
        Transaction.status == TransactionStatus.COMPLETED,
        Transaction.type == TransactionType.SUBSCRIPTION
    )
    
    if start_date:
        query = query.where(Transaction.created_at >= start_date)
    if end_date:
        query = query.where(Transaction.created_at <= end_date)
    
    result = await db.execute(query)
    return result.scalar() or 0.0


async def get_user_total_spent_kopeks(db: AsyncSession, user_id: int) -> int:
    """Get total amount spent by user in kopeks."""
    from sqlalchemy import func
    
    result = await db.execute(
        select(func.sum(Transaction.amount)).where(
            Transaction.user_id == user_id,
            Transaction.status == TransactionStatus.COMPLETED,
            Transaction.type == TransactionType.SUBSCRIPTION
        )
    )
    amount = result.scalar() or 0.0
    return int(amount * 100)


async def get_user_transactions_count(db: AsyncSession, user_id: int) -> int:
    """Get number of transactions for a user."""
    from sqlalchemy import func
    
    result = await db.execute(
        select(func.count(Transaction.id)).where(
            Transaction.user_id == user_id
        )
    )
    return result.scalar() or 0


async def check_tribute_payment_duplicate(
    db: AsyncSession,
    payment_id: str,
    amount_kopeks: int,
    user_telegram_id: int
) -> Optional[Transaction]:
    """Check if a tribute payment already exists."""
    result = await db.execute(
        select(Transaction).where(
            Transaction.payment_id == payment_id,
            Transaction.payment_method == "tribute"
        )
    )
    return result.scalar_one_or_none()


async def create_unique_tribute_transaction(
    db: AsyncSession,
    user_id: int,
    amount_kopeks: int,
    payment_id: str,
    **kwargs
) -> Transaction:
    """Create a unique tribute transaction."""
    transaction = Transaction(
        user_id=user_id,
        type=TransactionType.DEPOSIT,
        amount=amount_kopeks / 100.0,
        payment_id=payment_id,
        payment_method="tribute",
        currency=kwargs.get("currency", "RUB"),
        status=TransactionStatus.PENDING,
        description=kwargs.get("description", "Tribute payment")
    )
    db.add(transaction)
    await db.commit()
    await db.refresh(transaction)
    return transaction
