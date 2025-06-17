from sqlalchemy import Column, SmallInteger, String
from app.core.database import Base


class Region(Base):
    __tablename__ = "Region"

    region_code = Column(SmallInteger, primary_key=True, autoincrement=False)
    region_name = Column(String(100), nullable=False)
