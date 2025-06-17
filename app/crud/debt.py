from datetime import date
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models import Accrual, Debt

# Fixed reference rate used in README examples
REF_RATE = 7.50


async def calculate_debts(db: AsyncSession, taxpayer_id: str) -> List[Debt]:
    today = date.today()
    result = await db.execute(
        select(Accrual).where(
            Accrual.taxpayer_id == taxpayer_id,
            Accrual.due_date < today,
            Accrual.status != 'оплачено',
        )
    )
    accruals = result.scalars().all()

    for accrual in accruals:
        principal = float(accrual.amount) - float(accrual.paid_amount)
        if principal <= 0:
            continue
        debt_result = await db.execute(
            select(Debt).where(Debt.accrual_id == accrual.accrual_id)
        )
        debt = debt_result.scalar_one_or_none()
        if debt is None:
            debt = Debt(
                accrual_id=accrual.accrual_id,
                principal_amount=principal,
                penalty_amount=0,
                penalty_date=today,
                status='активно',
            )
            db.add(debt)
        else:
            debt.principal_amount = principal
            if debt.status == 'активно':
                days = (today - debt.penalty_date).days
                if days > 0:
                    debt.penalty_amount += round(
                        float(debt.principal_amount) * REF_RATE / 300 * days, 2
                    )
                    debt.penalty_date = today
            if principal == 0:
                debt.status = 'погашено'

    await db.commit()

    result = await db.execute(
        select(Debt).join(Accrual).where(Accrual.taxpayer_id == taxpayer_id)
    )
    return result.scalars().all()


async def get_total_debt(db: AsyncSession, taxpayer_id: str) -> float:
    """Return total active debt (principal + penalty) for a taxpayer."""
    debts = await calculate_debts(db, taxpayer_id)
    total = 0.0
    for debt in debts:
        if debt.status == "активно":
            total += float(debt.principal_amount) + float(debt.penalty_amount)
    return round(total, 2)
