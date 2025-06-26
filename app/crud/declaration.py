from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func

from .debt import calculate_debts

from app.models.taxdeclaration import TaxDeclaration
from app.schemas.declaration import TaxDeclarationWithAccrual
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
    # Accrual will be created automatically by database trigger
    await db.commit()
    # update debts for the taxpayer after new accrual
    await calculate_debts(db, declaration.taxpayer_id)
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


async def list_declarations_by_taxpayer(
    db: AsyncSession, taxpayer_id: str
) -> list[TaxDeclarationWithAccrual]:
    """Return declarations with related accrual IDs for a taxpayer."""
    stmt = (
        select(TaxDeclaration, Accrual.accrual_id)
        .join(Accrual, Accrual.declaration_id == TaxDeclaration.declaration_id)
        .where(TaxDeclaration.taxpayer_id == taxpayer_id)
        .order_by(TaxDeclaration.declaration_id)
    )
    result = await db.execute(stmt)
    items: list[TaxDeclarationWithAccrual] = []
    for decl, accrual_id in result.all():
        items.append(
            TaxDeclarationWithAccrual(
                declaration_id=decl.declaration_id,
                taxpayer_id=decl.taxpayer_id,
                tax_type_id=decl.tax_type_id,
                period=decl.period,
                submission_date=decl.submission_date,
                declared_tax_amount=decl.declared_tax_amount,
                status=decl.status,
                accrual_id=accrual_id,
            )
        )
    return items
