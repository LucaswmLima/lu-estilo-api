from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.product_model import Product

def ensure_unique_barcode(db: Session, barcode: str):
    if db.query(Product).filter_by(barcode=barcode).first():
        raise HTTPException(status_code=400, detail="Código de barras já cadastrado.")
