from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from .database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    cover = Column(String)
    price = Column(Integer)
    quantity = Column(Integer)
    stepper_id = Column(Integer, index=True)
    step_count = Column(Integer)
    floor_id = Column(Integer, index=True)


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, index=True)
    amount = Column(Integer)
    status = Column(String)
    pan = Column(String)
    trace = Column(String)
    rrn = Column(String)
    data1 = Column(String)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)