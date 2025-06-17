from sqlalchemy import Column, String, Enum, Date, SmallInteger
from app.core.database import Base


class Taxpayer(Base):
    __tablename__ = "Taxpayer"

    taxpayer_id = Column(String(12), primary_key=True)
    type = Column(Enum('F', 'U'), nullable=False)

    # Physical person
    last_name = Column(String(50))
    first_name = Column(String(50))
    middle_name = Column(String(50))
    birth_date = Column(Date)
    passport_no = Column(String(20))
    passport_date = Column(Date)

    # Legal entity
    company_name = Column(String(100))
    ogrn = Column(String(15))

    # Address
    region_code = Column(SmallInteger)
    city = Column(String(50))
    street = Column(String(100))
    house = Column(String(10))
    apartment = Column(String(10))
    phone = Column(String(20))
    email = Column(String(50))
