from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from app.core.database import get_session
from app.crud import (
    get_taxpayer,
    search_taxpayers,
    count_taxpayers,
    create_taxpayer,
    update_taxpayer,
)
from app.schemas import TaxpayerCreate, TaxpayerUpdate, TaxpayerRead

router = APIRouter()


@router.get('/search', response_model=List[TaxpayerRead])
async def search(
    query: str,
    page: int = 1,
    limit: int = 20,
    db: AsyncSession = Depends(get_session),
):
    offset = (page - 1) * limit
    return await search_taxpayers(db, query, limit=limit, offset=offset)


@router.get('/{taxpayer_id}', response_model=TaxpayerRead)
async def read_taxpayer(taxpayer_id: str, db: AsyncSession = Depends(get_session)):
    taxpayer = await get_taxpayer(db, taxpayer_id)
    if not taxpayer:
        raise HTTPException(status_code=404, detail='Taxpayer not found')
    return taxpayer


@router.post('/', response_model=TaxpayerRead)
async def create(tp: TaxpayerCreate, db: AsyncSession = Depends(get_session)):
    try:
        return await create_taxpayer(db, tp.dict())
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=400, detail='Taxpayer already exists')


@router.put('/{taxpayer_id}', response_model=TaxpayerRead)
async def update(taxpayer_id: str, tp: TaxpayerUpdate, db: AsyncSession = Depends(get_session)):
    taxpayer = await get_taxpayer(db, taxpayer_id)
    if not taxpayer:
        raise HTTPException(status_code=404, detail='Taxpayer not found')
    return await update_taxpayer(db, taxpayer, tp.dict(exclude_unset=True))
