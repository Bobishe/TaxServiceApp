from datetime import date
from pydantic import BaseModel, Field
from typing import Optional


class TaxpayerBase(BaseModel):
    taxpayer_id: str = Field(..., max_length=12)
    type: str
    last_name: Optional[str] = None
    first_name: Optional[str] = None
    middle_name: Optional[str] = None
    birth_date: Optional[date] = None
    passport_no: Optional[str] = None
    passport_date: Optional[date] = None
    company_name: Optional[str] = None
    ogrn: Optional[str] = None
    region_code: Optional[int] = None
    city: Optional[str] = None
    street: Optional[str] = None
    house: Optional[str] = None
    apartment: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None


class TaxpayerCreate(TaxpayerBase):
    pass


class TaxpayerUpdate(BaseModel):
    last_name: Optional[str] = None
    first_name: Optional[str] = None
    middle_name: Optional[str] = None
    birth_date: Optional[date] = None
    passport_no: Optional[str] = None
    passport_date: Optional[date] = None
    company_name: Optional[str] = None
    ogrn: Optional[str] = None
    region_code: Optional[int] = None
    city: Optional[str] = None
    street: Optional[str] = None
    house: Optional[str] = None
    apartment: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None


class TaxpayerRead(TaxpayerBase):
    class Config:
        orm_mode = True
