from sqlalchemy import Column, Integer, String, Enum
from app.core.database import Base


class Employee(Base):
    __tablename__ = "Employee"

    employee_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    position = Column(String(100), nullable=False)
    department = Column(String(100))
    role = Column(Enum('INSPECTOR', 'ADMIN'), nullable=False)
    phone = Column(String(20))
    email = Column(String(50))
