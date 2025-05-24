from sqlalchemy.orm import Session
from typing import List, Optional
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException

from app.models import Product
from app.schemas.product_schema import ProductCreate, ProductUpdate
#from app.validations. import ensure_product_not_in_orders
from app.validations.product_validation import ensure_unique_barcode



def get_products(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    section: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    available: Optional[bool] = None,
) -> List[Product]:
    query = db.query(Product)

    if section:
        query = query.filter(Product.section == section)
    if min_price is not None:
        query = query.filter(Product.price >= min_price)
    if max_price is not None:
        query = query.filter(Product.price <= max_price)
    if available is True:
        query = query.filter(Product.stock > 0)
    elif available is False:
        query = query.filter(Product.stock <= 0)

    return query.offset(skip).limit(limit).all()


def get_product_by_id(db: Session, product_id: int) -> Optional[Product]:
    return db.get(Product, product_id)


def create_product(db: Session, product: ProductCreate):
    ensure_unique_barcode(db, product.barcode)
    db_product = Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def update_product(db: Session, product_id: int, data: ProductUpdate) -> Optional[Product]:
    product = db.get(Product, product_id)
    if not product:
        return None

    updated_data = data.model_dump(exclude_unset=True)

    #if "price" in updated_data or "name" in updated_data or "stock" in updated_data:
        #ensure_product_not_in_orders(db, product_id)

    for field, value in updated_data.items():
        setattr(product, field, value)

    db.commit()
    db.refresh(product)
    return product


def delete_product(db: Session, product_id: int) -> bool:
    product = db.get(Product, product_id)
    if not product:
        return False

    #ensure_product_not_in_orders(db, product_id)

    db.delete(product)
    db.commit()
    return True
