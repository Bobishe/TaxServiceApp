from sqlalchemy import Column, Integer, String, Date, Enum, Numeric
from sqlalchemy.orm import relationship
from app.core.database import Base


class TaxDeclaration(Base):
    __tablename__ = "TaxDeclaration"

    declaration_id = Column(Integer, primary_key=True, autoincrement=True)
    taxpayer_id = Column(String(12), nullable=False)
    tax_type_id = Column(String(10), nullable=False)
    period = Column(Integer, nullable=False)
    submission_date = Column(Date, nullable=False)
    declared_tax_amount = Column(Numeric(15, 2), nullable=False)
    status = Column(
        Enum('принята', 'на проверке', 'выявлены ошибки', 'утверждена'),
        default='принята'
    )
