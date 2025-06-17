from sqlalchemy import Column, String, Text
from app.core.database import Base


class TaxType(Base):
    __tablename__ = "TaxType"

    tax_type_id = Column(String(10), primary_key=True)
    tax_name = Column(String(100), nullable=False)
    description = Column(Text)
