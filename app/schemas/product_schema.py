from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import date

class ProductBase(BaseModel):
    description: str
    price: float
    barcode: str
    section: str
    stock: int
    expiration_date: Optional[date] = None

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    description: Optional[str]
    price: Optional[float]
    barcode: Optional[str]
    section: Optional[str]
    stock: Optional[int]
    expiration_date: Optional[date]

class ProductOut(ProductBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
