from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

BaseProduct = declarative_base()
class Product(BaseProduct):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, index=True)
    price = Column(Float, nullable=False, index=True)
    created_time = Column(DateTime(timezone=True), server_default=func.now())
    description = Column(String)
    quantity = Column(Integer, nullable=False)
