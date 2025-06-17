from sqlalchemy import Column, Integer, String, Date, Enum, Numeric, Text
from app.core.database import Base


class Inspection(Base):
    __tablename__ = "Inspection"

    inspection_id = Column(Integer, primary_key=True, autoincrement=True)
    taxpayer_id = Column(String(12), nullable=False)
    employee_id = Column(Integer, nullable=False)
    type = Column(Enum('камеральная', 'выездная'), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date)
    result = Column(Text)
    additional_tax = Column(Numeric(15, 2), default=0)
    fine_amount = Column(Numeric(15, 2), default=0)
