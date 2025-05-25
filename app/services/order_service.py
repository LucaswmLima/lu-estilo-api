from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List
from app.models.order_model import Order, OrderProduct
from app.schemas.order_schema import OrderCreate, OrderUpdate
from app.models.product_model import Product

def create_order(db: Session, order_in: OrderCreate, user_id: int):
    # Validar estoque dos produtos
    for item in order_in.products:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail=f"Produto {item.product_id} não encontrado")
        if product.stock < item.quantity:
            raise HTTPException(
                status_code=400,
                detail=f"Estoque insuficiente para produto {product.description}",
            )

    # Criar pedido
    db_order = Order(client_id=order_in.client_id, status=order_in.status, created_by=user_id)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    # Criar os relacionamentos order_products e atualizar estoque
    for item in order_in.products:
        order_product = OrderProduct(order_id=db_order.id, product_id=item.product_id, quantity=item.quantity)
        db.add(order_product)

        # Atualiza estoque
        product = db.query(Product).filter(Product.id == item.product_id).first()
        product.stock -= item.quantity
        db.add(product)

    db.commit()
    db.refresh(db_order)
    return db_order

def get_order(db: Session, order_id: int, user_id: int, is_admin: bool):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")

    # Se não for admin, só permite ver se for dono
    if not is_admin and order.created_by != user_id:
        raise HTTPException(status_code=403, detail="Acesso negado")
    return order

def list_orders(db: Session, user_id: int, is_admin: bool):
    if is_admin:
        return db.query(Order).all()
    else:
        return db.query(Order).filter(Order.created_by == user_id).all()

def update_order(db: Session, order_id: int, order_update: OrderUpdate, user_id: int, is_admin: bool):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")

    if not is_admin and order.created_by != user_id:
        raise HTTPException(status_code=403, detail="Acesso negado")

    if order_update.status is not None:
        order.status = order_update.status

    db.add(order)
    db.commit()
    db.refresh(order)
    return order

def delete_order(db: Session, order_id: int, user_id: int, is_admin: bool):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")

    if not is_admin and order.created_by != user_id:
        raise HTTPException(status_code=403, detail="Acesso negado")

    db.delete(order)
    db.commit()
    return {"detail": "Pedido deletado com sucesso"}
