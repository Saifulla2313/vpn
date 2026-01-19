"""
Webhook endpoints for payment providers
"""
import logging
import hashlib
import hmac
from typing import Optional

from fastapi import APIRouter, Request, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.connection import get_db_session
from app.database.crud.users import get_user_by_telegram_id, update_user_balance
from app.database.crud.transactions import (
    get_transaction_by_external_id,
    update_transaction_status,
)
from app.config import settings

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/webhook", tags=["webhooks"])


@router.post("/yookassa")
async def yookassa_webhook(
    request: Request,
    db: AsyncSession = Depends(get_db_session),
):
    """
    Handle YooKassa payment notifications.
    
    YooKassa sends notifications when payment status changes.
    Docs: https://yookassa.ru/developers/using-api/webhooks
    """
    try:
        body = await request.json()
    except Exception as e:
        logger.error(f"Failed to parse YooKassa webhook body: {e}")
        raise HTTPException(status_code=400, detail="Invalid JSON body")

    event_type = body.get("event")
    payment_object = body.get("object", {})
    
    logger.info(f"YooKassa webhook received: event={event_type}, payment_id={payment_object.get('id')}")
    
    if event_type == "payment.succeeded":
        await _handle_yookassa_payment_succeeded(db, payment_object)
    elif event_type == "payment.canceled":
        await _handle_yookassa_payment_canceled(db, payment_object)
    elif event_type == "payment.waiting_for_capture":
        logger.info(f"Payment waiting for capture: {payment_object.get('id')}")
    else:
        logger.warning(f"Unknown YooKassa event type: {event_type}")
    
    return {"status": "ok"}


async def _handle_yookassa_payment_succeeded(
    db: AsyncSession,
    payment_object: dict,
):
    """Process successful YooKassa payment"""
    payment_id = payment_object.get("id")
    metadata = payment_object.get("metadata", {})
    amount_info = payment_object.get("amount", {})
    
    amount_value = float(amount_info.get("value", 0))
    user_id = metadata.get("user_id")
    transaction_id = metadata.get("transaction_id")
    
    logger.info(
        f"YooKassa payment succeeded: payment_id={payment_id}, "
        f"amount={amount_value}, user_id={user_id}, transaction_id={transaction_id}"
    )
    
    if not user_id:
        logger.error(f"No user_id in payment metadata: {payment_id}")
        return
    
    try:
        user_id_int = int(user_id)
    except (ValueError, TypeError):
        logger.error(f"Invalid user_id format: {user_id}")
        return
    
    user = await get_user_by_telegram_id(db, user_id_int)
    if not user:
        logger.error(f"User not found for telegram_id: {user_id_int}")
        return
    
    if transaction_id:
        existing_tx = await get_transaction_by_external_id(db, payment_id)
        if existing_tx and existing_tx.status == "completed":
            logger.warning(f"Transaction already processed: {payment_id}")
            return
        
        if existing_tx:
            await update_transaction_status(db, existing_tx.id, "completed")
    
    new_balance = user.balance + amount_value
    await update_user_balance(db, user.id, new_balance)
    
    logger.info(
        f"Balance updated for user {user_id_int}: "
        f"{user.balance} -> {new_balance} (+{amount_value})"
    )


async def _handle_yookassa_payment_canceled(
    db: AsyncSession,
    payment_object: dict,
):
    """Process canceled YooKassa payment"""
    payment_id = payment_object.get("id")
    metadata = payment_object.get("metadata", {})
    cancellation_details = payment_object.get("cancellation_details", {})
    
    logger.info(
        f"YooKassa payment canceled: payment_id={payment_id}, "
        f"reason={cancellation_details.get('reason')}"
    )
    
    existing_tx = await get_transaction_by_external_id(db, payment_id)
    if existing_tx:
        await update_transaction_status(db, existing_tx.id, "failed")
        logger.info(f"Transaction marked as failed: {payment_id}")
