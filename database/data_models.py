from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Lead(Base):
    __tablename__ = 'leads'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    email = Column(String(100))
    source = Column(String(100))
    status = Column(String(100))
    interest_level = Column(String(100))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    sales_person_id = Column(Integer, ForeignKey('salespeople.id'))


class Salesperson(Base):
    __tablename__ = 'salespeople'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))





