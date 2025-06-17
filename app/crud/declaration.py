from datetime import timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func

from app.models.taxdeclaration import TaxDeclaration
from app.models.accrual import Accrual


async def get_declaration(db: AsyncSession, declaration_id: int):
    result = await db.execute(
        select(TaxDeclaration).where(TaxDeclaration.declaration_id == declaration_id)
    )
    return result.scalar_one_or_none()


async def create_declaration(db: AsyncSession, data: dict) -> TaxDeclaration:
    declaration = TaxDeclaration(**data)
    db.add(declaration)
    await db.flush()

    accrual = Accrual(
        taxpayer_id=declaration.taxpayer_id,
        tax_type_id=declaration.tax_type_id,
        period=declaration.period,
        amount=declaration.declared_tax_amount,
        due_date=declaration.submission_date + timedelta(days=90),
        declaration_id=declaration.declaration_id,
    )
    db.add(accrual)
    await db.commit()
    await db.refresh(declaration)
    return declaration


async def search_declarations(
    db: AsyncSession, query: str, limit: int = 20, offset: int = 0
) -> list[TaxDeclaration]:
    """Search declarations by taxpayer ID or tax type."""
    stmt = select(TaxDeclaration)
    if query:
        like_pattern = f"%{query}%"
        stmt = stmt.where(
            (TaxDeclaration.taxpayer_id == query)
            | (TaxDeclaration.tax_type_id.ilike(like_pattern))
        )
    stmt = stmt.order_by(TaxDeclaration.declaration_id).offset(offset).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()


async def count_declarations(db: AsyncSession, query: str) -> int:
    """Return number of declarations matching the query."""
    stmt = select(func.count()).select_from(TaxDeclaration)
    if query:
        like_pattern = f"%{query}%"
        stmt = stmt.where(
            (TaxDeclaration.taxpayer_id == query)
            | (TaxDeclaration.tax_type_id.ilike(like_pattern))
        )
    result = await db.execute(stmt)
    return result.scalar_one()
