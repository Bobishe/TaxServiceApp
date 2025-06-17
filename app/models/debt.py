from sqlalchemy import Column, Integer, Numeric, Date, Enum
from app.core.database import Base


class Debt(Base):
    __tablename__ = "Debt"

    debt_id = Column(Integer, primary_key=True, autoincrement=True)
    accrual_id = Column(Integer, nullable=False, unique=True)
    principal_amount = Column(Numeric(15, 2), nullable=False)
    penalty_amount = Column(Numeric(15, 2), nullable=False, default=0)
    penalty_date = Column(Date, nullable=False)
    status = Column(Enum('активно', 'погашено'), default='активно')
