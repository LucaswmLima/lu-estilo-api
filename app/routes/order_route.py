from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from app.schemas.order_schema import OrderCreate, OrderOut, OrderUpdate
from app.db.database import get_db
from app.services.order_service import create_order, get_order, list_orders, update_order, delete_order
from app.routes.auth_route import get_current_user, require_admin

router = APIRouter(prefix="/orders", tags=["orders"])

@router.post("/", response_model=OrderOut, status_code=status.HTTP_201_CREATED)
def create_new_order(order_in: OrderCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    order = create_order(db, order_in, current_user["id"])
    return order

@router.get("/", response_model=List[OrderOut])
def get_orders(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    is_admin = current_user.get("is_admin", False)
    orders = list_orders(db, current_user["id"], is_admin)
    return orders

@router.get("/{order_id}", response_model=OrderOut)
def get_order_by_id(order_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    is_admin = current_user.get("is_admin", False)
    order = get_order(db, order_id, current_user["id"], is_admin)
    return order

@router.put("/{order_id}", response_model=OrderOut)
def update_order_by_id(order_id: int, order_update: OrderUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    is_admin = current_user.get("is_admin", False)
    order = update_order(db, order_id, order_update, current_user["id"], is_admin)
    return order

@router.delete("/{order_id}")
def delete_order_by_id(order_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    is_admin = current_user.get("is_admin", False)
    return delete_order(db, order_id, current_user["id"], is_admin)
