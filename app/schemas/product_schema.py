from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import date

class ProductImageOut(BaseModel):
    id: int
    path: str
    model_config = ConfigDict(from_attributes=True)

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
    description: Optional[str] = None
    price: Optional[float] = None
    barcode: Optional[str] = None
    section: Optional[str] = None
    stock: Optional[int] = None
    expiration_date: Optional[date] = None

class ProductOut(ProductBase):
    id: int
    images: List[ProductImageOut] = []
    model_config = ConfigDict(from_attributes=True)
