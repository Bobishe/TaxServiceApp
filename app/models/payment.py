from sqlalchemy import Column, Integer, String, Date, Numeric
from app.core.database import Base


class Payment(Base):
    __tablename__ = "Payment"

    payment_id = Column(Integer, primary_key=True, autoincrement=True)
    taxpayer_id = Column(String(12), nullable=False)
    accrual_id = Column(Integer, nullable=False)
    payment_date = Column(Date, nullable=False)
    amount = Column(Numeric(15, 2), nullable=False)
