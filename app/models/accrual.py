from sqlalchemy import Column, Integer, String, Numeric, Date, Enum
from app.core.database import Base


class Accrual(Base):
    __tablename__ = "Accrual"

    accrual_id = Column(Integer, primary_key=True, autoincrement=True)
    taxpayer_id = Column(String(12), nullable=False)
    tax_type_id = Column(String(10), nullable=False)
    period = Column(Integer, nullable=False)
    amount = Column(Numeric(15, 2), nullable=False)
    paid_amount = Column(Numeric(15, 2), nullable=False, default=0)
    due_date = Column(Date, nullable=False)
    declaration_id = Column(Integer)
    status = Column(
        Enum('начислено', 'оплачено частично', 'оплачено', 'просрочено'),
        default='начислено'
    )
