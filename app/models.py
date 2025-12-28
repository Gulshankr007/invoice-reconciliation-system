from sqlalchemy import Column, Integer, String, Float
from .database import Base

class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True)
    invoice_number = Column(String, unique=True)
    vendor = Column(String)
    amount = Column(Float)
    status = Column(String, default="UNMATCHED")


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True)
    vendor = Column(String)
    paid_amount = Column(Float)
