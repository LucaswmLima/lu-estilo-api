import os
import shutil
from fastapi import UploadFile, HTTPException
from sqlalchemy.orm import Session
from app.models.product_image import ProductImage
from app.models.product import Product
from uuid import uuid4

UPLOAD_DIR = "uploads"

def save_product_image(db: Session, product_id: int, file: UploadFile) -> ProductImage:
    product = db.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    ext = os.path.splitext(file.filename)[-1]
    filename = f"{uuid4().hex}{ext}"
    path = os.path.join(UPLOAD_DIR, filename)

    os.makedirs(UPLOAD_DIR, exist_ok=True)
    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    image = ProductImage(product_id=product_id, path=path)
    db.add(image)
    db.commit()
    db.refresh(image)
    return image

def delete_product_image(db: Session, product_id: int, image_id: int):
    image = db.query(ProductImage).filter_by(id=image_id, product_id=product_id).first()
    if not image:
        raise HTTPException(status_code=404, detail="Imagem não encontrada")

    if os.path.exists(image.path):
        os.remove(image.path)

    db.delete(image)
    db.commit()
