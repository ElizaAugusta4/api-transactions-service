from sqlalchemy import Column, Integer, String, DateTime, Numeric, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime, timezone

Base = declarative_base()

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("accounts.id", ondelete="CASCADE"), nullable=False, index=True)
    type = Column(String(20), nullable=False)
    amount = Column(Numeric(12, 2), nullable=False)
    description = Column(String(255), nullable=True)
    occurred_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False, index=True)
    category = Column(String(50), nullable=True, index=True)
