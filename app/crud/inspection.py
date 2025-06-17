from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models import Inspection


async def get_inspection(db: AsyncSession, inspection_id: int) -> Optional[Inspection]:
    result = await db.execute(
        select(Inspection).where(Inspection.inspection_id == inspection_id)
    )
    return result.scalar_one_or_none()


async def list_inspections(db: AsyncSession, taxpayer_id: str) -> List[Inspection]:
    result = await db.execute(
        select(Inspection).where(Inspection.taxpayer_id == taxpayer_id)
    )
    return result.scalars().all()


async def create_inspection(db: AsyncSession, data: dict) -> Inspection:
    inspection = Inspection(**data)
    db.add(inspection)
    await db.commit()
    await db.refresh(inspection)
    return inspection
