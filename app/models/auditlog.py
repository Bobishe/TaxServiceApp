from sqlalchemy import Column, Integer, String, Text, Enum, TIMESTAMP
from sqlalchemy.sql import func
from app.core.database import Base


class AuditLog(Base):
    __tablename__ = "AuditLog"

    audit_id = Column(Integer, primary_key=True, autoincrement=True)
    event_time = Column(TIMESTAMP, server_default=func.current_timestamp())
    user_name = Column(String(100), nullable=False)
    action_type = Column(Enum('INSERT', 'UPDATE', 'DELETE'), nullable=False)
    table_name = Column(String(64), nullable=False)
    record_id = Column(String(64), nullable=False)
    old_values = Column(Text)
    new_values = Column(Text)
