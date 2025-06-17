from datetime import date
from decimal import Decimal

from pydantic import BaseModel


class PaymentBase(BaseModel):
    taxpayer_id: str
    accrual_id: int
    payment_date: date
    amount: Decimal


class PaymentCreate(PaymentBase):
    pass


class PaymentRead(PaymentBase):
    payment_id: int

    class Config:
        orm_mode = True
