from sqlalchemy import Column, Integer, String, Float, DateTime
from .database import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, index=True)
    amount = Column(Float)
    status = Column(String)
    failure_reason = Column(String, nullable=True)
    payment_method = Column(String)
    timestamp = Column(DateTime)


class AgentAction(Base):
    __tablename__ = "agent_actions"

    id = Column(Integer, primary_key=True, index=True)
    action_type = Column(String)
    title = Column(String)
    description = Column(String)
    status = Column(String)
    created_at = Column(DateTime)