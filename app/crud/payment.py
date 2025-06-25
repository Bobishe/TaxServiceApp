from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func, or_

from .debt import calculate_debts

from app.models.payment import Payment
from app.models.accrual import Accrual


async def get_payment(db: AsyncSession, payment_id: int):
    result = await db.execute(select(Payment).where(Payment.payment_id == payment_id))
    return result.scalar_one_or_none()


async def create_payment(db: AsyncSession, data: dict) -> Payment:
    accrual = await db.get(Accrual, data["accrual_id"])
    if accrual is None or accrual.taxpayer_id != data["taxpayer_id"]:
        raise ValueError("Accrual not found")
    if accrual.paid_amount + data["amount"] > accrual.amount:
        raise ValueError("Payment exceeds accrual amount")

    payment = Payment(**data)
    db.add(payment)

    accrual.paid_amount += data["amount"]
    if accrual.paid_amount == accrual.amount:
        accrual.status = "оплачено"
    else:
        accrual.status = "оплачено частично"

    await db.commit()
    await db.refresh(payment)

    # Recalculate debts for the taxpayer after payment
    await calculate_debts(db, data["taxpayer_id"])

    return payment


async def search_payments(
    db: AsyncSession, query: str, limit: int = 20, offset: int = 0
) -> list[Payment]:
    stmt = select(Payment)
    if query:
        conditions = [Payment.taxpayer_id == query]
        if query.isdigit():
            conditions.append(Payment.payment_id == int(query))
        stmt = stmt.where(or_(*conditions))
    stmt = stmt.order_by(Payment.payment_id).offset(offset).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()


async def count_payments(db: AsyncSession, query: str) -> int:
    stmt = select(func.count()).select_from(Payment)
    if query:
        conditions = [Payment.taxpayer_id == query]
        if query.isdigit():
            conditions.append(Payment.payment_id == int(query))
        stmt = stmt.where(or_(*conditions))
    result = await db.execute(stmt)
    return result.scalar_one()
