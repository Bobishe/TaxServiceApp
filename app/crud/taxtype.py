from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.taxtype import TaxType

async def list_tax_types(db: AsyncSession) -> list[TaxType]:
    result = await db.execute(select(TaxType).order_by(TaxType.tax_type_id))
    return result.scalars().all()
