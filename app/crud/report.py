from typing import List, Dict
from decimal import Decimal

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Payment, Accrual, TaxType, Taxpayer, Debt
from .debt import calculate_debts


async def tax_revenue_report(db: AsyncSession) -> List[Dict]:
    result = await db.execute(
        select(
            Accrual.tax_type_id,
            TaxType.tax_name,
            func.sum(Payment.amount).label('total_amount'),
        )
        .join(Accrual, Payment.accrual_id == Accrual.accrual_id)
        .join(TaxType, TaxType.tax_type_id == Accrual.tax_type_id)
        .group_by(Accrual.tax_type_id, TaxType.tax_name)
    )
    rows = result.all()
    return [
        {
            'tax_type_id': r.tax_type_id,
            'tax_name': r.tax_name,
            'total_amount': r.total_amount,
        }
        for r in rows
    ]


async def debtors_list(db: AsyncSession) -> List[Dict]:
    # Update debts for all taxpayers
    taxpayer_ids = (await db.execute(select(Taxpayer.taxpayer_id))).scalars().all()
    for tid in taxpayer_ids:
        await calculate_debts(db, tid)

    result = await db.execute(
        select(
            Taxpayer.taxpayer_id,
            Taxpayer.last_name,
            Taxpayer.first_name,
            Taxpayer.middle_name,
            Taxpayer.company_name,
            func.sum(Debt.principal_amount + Debt.penalty_amount).label('total_debt'),
        )
        .join(Accrual, Accrual.taxpayer_id == Taxpayer.taxpayer_id)
        .join(Debt, Debt.accrual_id == Accrual.accrual_id)
        .where(Debt.status == 'активно')
        .group_by(
            Taxpayer.taxpayer_id,
            Taxpayer.last_name,
            Taxpayer.first_name,
            Taxpayer.middle_name,
            Taxpayer.company_name,
        )
    )
    rows = result.all()

    def build_name(row):
        if row.company_name:
            return row.company_name
        parts = [row.last_name, row.first_name, row.middle_name]
        return ' '.join([p for p in parts if p])

    return [
        {
            'taxpayer_id': r.taxpayer_id,
            'name': build_name(r),
            'total_debt': r.total_debt,
        }
        for r in rows
    ]
