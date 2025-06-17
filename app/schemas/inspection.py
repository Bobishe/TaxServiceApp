from datetime import date
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel


class InspectionBase(BaseModel):
    taxpayer_id: str
    employee_id: int
    type: str
    start_date: date
    end_date: Optional[date] = None
    result: Optional[str] = None
    additional_tax: Decimal = Decimal('0')
    fine_amount: Decimal = Decimal('0')


class InspectionCreate(InspectionBase):
    pass


class InspectionRead(InspectionBase):
    inspection_id: int

    class Config:
        orm_mode = True
