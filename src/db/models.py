from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text
from datetime import datetime
from src.db.database import Base

class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    city = Column(String, nullable=False)

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(String, primary_key=True, index=True)  # uuid
    ts = Column(DateTime, default=datetime.utcnow)

    endpoint = Column(String, nullable=False)
    role = Column(String, nullable=False)
    operation = Column(String, nullable=False)
    table = Column(String, nullable=True)

    allowed = Column(Boolean, default=True)
    status = Column(Integer, default=200)
    reason = Column(Text, nullable=True)

    raw_text = Column(Text, nullable=True)
    result_count = Column(Integer, nullable=True)
