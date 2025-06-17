from datetime import timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

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
