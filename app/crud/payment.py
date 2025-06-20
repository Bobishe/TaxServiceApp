from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.payment import Payment
from app.models.accrual import Accrual


async def get_payment(db: AsyncSession, payment_id: int):
    result = await db.execute(select(Payment).where(Payment.payment_id == payment_id))
    return result.scalar_one_or_none()


async def create_payment(db: AsyncSession, data: dict) -> Payment:
    accrual = await db.get(Accrual, data['accrual_id'])
    if accrual is None or accrual.taxpayer_id != data['taxpayer_id']:
        raise ValueError('Accrual not found')
    if accrual.paid_amount + data['amount'] > accrual.amount:
        raise ValueError('Payment exceeds accrual amount')

    payment = Payment(**data)
    db.add(payment)

    accrual.paid_amount += data['amount']
    if accrual.paid_amount == accrual.amount:
        accrual.status = 'оплачено'
    else:
        accrual.status = 'оплачено частично'

    await db.commit()
    await db.refresh(payment)
    return payment
