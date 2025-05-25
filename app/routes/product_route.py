from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List, Optional
import os

from app.db.database import get_db
from app.schemas.product_schema import ProductCreate, ProductUpdate, ProductOut
from app.services.product_service import (
    get_products as service_get_products,
    get_product_by_id,
    create_product as service_create_product,
    update_product as service_update_product,
    delete_product as service_delete_product,
)
from app.routes.auth_route import get_current_user, require_admin

IMAGE_FOLDER = "app/static/images"

router = APIRouter(prefix="/products", tags=["products"])

@router.get("/", response_model=List[ProductOut])
def get_products(
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
    skip: int = 0,
    limit: int = 10,
    section: Optional[str] = Query(None),
    min_price: Optional[float] = Query(None),
    max_price: Optional[float] = Query(None),
    available: Optional[bool] = Query(None),
):
    return service_get_products(db, skip, limit, section, min_price, max_price, available)

@router.post("/", response_model=ProductOut)
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db),
    user=Depends(require_admin),
):
    return service_create_product(db, product)

@router.get("/{product_id}", response_model=ProductOut)
def get_product(
    product_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    product = get_product_by_id(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return product

@router.put("/{product_id}", response_model=ProductOut)
def update_product(
    product_id: int,
    update_data: ProductUpdate,
    db: Session = Depends(get_db),
    user=Depends(require_admin),
):
    product = service_update_product(db, product_id, update_data)
    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return product

@router.delete("/{product_id}")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    user=Depends(require_admin),
):
    success = service_delete_product(db, product_id)
    if not success:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return {"detail": "Produto deletado com sucesso"}

# Rota para servir imagens estáticas dos produtos
@router.get("/images/{image_filename}")
def serve_product_image(image_filename: str):
    file_path = os.path.join(IMAGE_FOLDER, image_filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Imagem não encontrada")
    return FileResponse(file_path)
