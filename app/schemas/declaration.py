from datetime import date
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel


class TaxDeclarationBase(BaseModel):
    taxpayer_id: str
    tax_type_id: str
    period: int
    submission_date: date
    declared_tax_amount: Decimal


class TaxDeclarationCreate(TaxDeclarationBase):
    pass


class TaxDeclarationRead(TaxDeclarationBase):
    declaration_id: int
    status: Optional[str] = None

    class Config:
        orm_mode = True
