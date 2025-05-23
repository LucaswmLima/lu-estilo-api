from sqlalchemy import Column, Integer, String, Float, Date, Boolean
from app.db.database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    barcode = Column(String, unique=True, nullable=False)
    section = Column(String, nullable=False)
    stock = Column(Integer, default=0)
    expiration_date = Column(Date, nullable=True)
    available = Column(Boolean, default=True)
