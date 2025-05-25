from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date

from app.schemas.order_schema import OrderCreate, OrderOut, OrderUpdate
from app.services.order_service import (
    create_order,
    get_order,
    get_orders,
    update_order_status,
    delete_order,
)
from app.dependencies import get_db, get_current_user
from app.models.user_model import User

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("/", response_model=OrderOut)
def create_new_order(
    order_data: OrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_order(db, order_data)


@router.get("/", response_model=List[OrderOut])
def list_orders(
    db: Session = Depends(get_db),
    id: Optional[int] = None,
    client_id: Optional[int] = None,
    section: Optional[str] = None,
    status: Optional[str] = None,
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    current_user: User = Depends(get_current_user),
):
    return get_orders(db, id, client_id, section, status, start_date, end_date)


@router.get("/{order_id}", response_model=OrderOut)
def get_order_by_id(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_order(db, order_id)


@router.put("/{order_id}", response_model=OrderOut)
def update_order(
    order_id: int,
    update_data: OrderUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return update_order_status(db, order_id, update_data.status)


@router.delete("/{order_id}")
def delete_order_route(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    delete_order(db, order_id)
    return {"message": "Pedido deletado com sucesso"}