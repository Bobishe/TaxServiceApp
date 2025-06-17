from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.crud import tax_revenue_report, debtors_list
from app.schemas import TaxRevenueItem, DebtorItem

router = APIRouter()


@router.get('/payments', response_model=List[TaxRevenueItem])
async def payments_report(db: AsyncSession = Depends(get_session)):
    return await tax_revenue_report(db)


@router.get('/debtors', response_model=List[DebtorItem])
async def debtors_report(db: AsyncSession = Depends(get_session)):
    return await debtors_list(db)
