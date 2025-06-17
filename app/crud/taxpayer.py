from typing import List, Optional
from sqlalchemy.future import select
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.taxpayer import Taxpayer


async def get_taxpayer(db: AsyncSession, taxpayer_id: str) -> Optional[Taxpayer]:
    result = await db.execute(select(Taxpayer).where(Taxpayer.taxpayer_id == taxpayer_id))
    return result.scalar_one_or_none()


async def search_taxpayers(
    db: AsyncSession,
    query: str,
    limit: int = 20,
    offset: int = 0,
) -> List[Taxpayer]:
    """Search taxpayers with optional pagination."""
    stmt = select(Taxpayer)
    if query:
        like_pattern = f"%{query}%"
        stmt = stmt.where(
            (Taxpayer.taxpayer_id == query)
            | (Taxpayer.last_name.ilike(like_pattern))
            | (Taxpayer.first_name.ilike(like_pattern))
            | (Taxpayer.middle_name.ilike(like_pattern))
            | (Taxpayer.company_name.ilike(like_pattern))
        )
    stmt = stmt.order_by(Taxpayer.taxpayer_id).offset(offset).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()


async def count_taxpayers(db: AsyncSession, query: str) -> int:
    """Return number of taxpayers matching the query."""
    stmt = select(func.count()).select_from(Taxpayer)
    if query:
        like_pattern = f"%{query}%"
        stmt = stmt.where(
            (Taxpayer.taxpayer_id == query)
            | (Taxpayer.last_name.ilike(like_pattern))
            | (Taxpayer.first_name.ilike(like_pattern))
            | (Taxpayer.middle_name.ilike(like_pattern))
            | (Taxpayer.company_name.ilike(like_pattern))
        )
    result = await db.execute(stmt)
    return result.scalar_one()


async def create_taxpayer(db: AsyncSession, data: dict) -> Taxpayer:
    taxpayer = Taxpayer(**data)
    db.add(taxpayer)
    await db.commit()
    await db.refresh(taxpayer)
    return taxpayer


async def update_taxpayer(db: AsyncSession, taxpayer: Taxpayer, data: dict) -> Taxpayer:
    for key, value in data.items():
        setattr(taxpayer, key, value)
    await db.commit()
    await db.refresh(taxpayer)
    return taxpayer
