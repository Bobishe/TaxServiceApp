from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.crud import get_payment, create_payment
from app.schemas import PaymentCreate, PaymentRead

router = APIRouter()


@router.post('/', response_model=PaymentRead)
async def create(pay: PaymentCreate, db: AsyncSession = Depends(get_session)):
    try:
        return await create_payment(db, pay.dict())
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get('/{payment_id}', response_model=PaymentRead)
async def read(payment_id: int, db: AsyncSession = Depends(get_session)):
    payment = await get_payment(db, payment_id)
    if not payment:
        raise HTTPException(status_code=404, detail='Payment not found')
    return payment
