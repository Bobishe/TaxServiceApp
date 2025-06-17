from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.crud import calculate_debts
from app.schemas import DebtRead

router = APIRouter()


@router.get('/{taxpayer_id}', response_model=List[DebtRead])
async def read_debts(taxpayer_id: str, db: AsyncSession = Depends(get_session)):
    return await calculate_debts(db, taxpayer_id)
