from decimal import Decimal
from pydantic import BaseModel


class TaxRevenueItem(BaseModel):
    tax_type_id: str
    tax_name: str
    total_amount: Decimal


class DebtorItem(BaseModel):
    taxpayer_id: str
    name: str
    total_debt: Decimal
