from datetime import date
from decimal import Decimal
from pydantic import BaseModel


class DebtRead(BaseModel):
    debt_id: int
    accrual_id: int
    principal_amount: Decimal
    penalty_amount: Decimal
    penalty_date: date
    status: str

    class Config:
        orm_mode = True
