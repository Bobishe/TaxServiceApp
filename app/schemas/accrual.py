from datetime import date
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel


class AccrualRead(BaseModel):
    accrual_id: int
    taxpayer_id: str
    tax_type_id: str
    period: int
    amount: Decimal
    paid_amount: Decimal
    due_date: date
    declaration_id: Optional[int] = None
    status: str

    class Config:
        orm_mode = True
