from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.crud import (
    get_inspection,
    list_inspections,
    create_inspection,
)
from app.schemas import InspectionCreate, InspectionRead

router = APIRouter()


@router.post('/', response_model=InspectionRead)
async def create(ins: InspectionCreate, db: AsyncSession = Depends(get_session)):
    return await create_inspection(db, ins.dict())


@router.get('/{inspection_id}', response_model=InspectionRead)
async def read(inspection_id: int, db: AsyncSession = Depends(get_session)):
    inspection = await get_inspection(db, inspection_id)
    if not inspection:
        raise HTTPException(status_code=404, detail='Inspection not found')
    return inspection


@router.get('/by_taxpayer/{taxpayer_id}', response_model=List[InspectionRead])
async def by_taxpayer(taxpayer_id: str, db: AsyncSession = Depends(get_session)):
    return await list_inspections(db, taxpayer_id)
