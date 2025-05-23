from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.schemas.client import ClientCreate, ClientOut, ClientUpdate
from app.models import models
from app.db.database import get_db
from app.utils.validations import ensure_unique_email, ensure_unique_cpf

router = APIRouter(prefix="/clients", tags=["Clients"])


# Listar todos os clientes com filtros e paginação
@router.get("/", response_model=List[ClientOut])
def get_clients(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 10,
    name: Optional[str] = Query(None),
    email: Optional[str] = Query(None),
):
    query = db.query(models.Client)

    if name:
        query = query.filter(models.Client.name.contains(name))
    if email:
        query = query.filter(models.Client.email.contains(email))

    return query.offset(skip).limit(limit).all()


# Criar um novo cliente
@router.post("/", response_model=ClientOut)
def create_client(client: ClientCreate, db: Session = Depends(get_db)):
    ensure_unique_email(db, client.email)
    ensure_unique_cpf(db, client.cpf)

    db_client = models.Client(**client.dict())
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client


# Buscar um cliente por ID
@router.get("/{client_id}", response_model=ClientOut)
def get_client(client_id: int, db: Session = Depends(get_db)):
    client = db.query(models.Client).get(client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return client


# Atualiza um cliente
@router.put("/{client_id}", response_model=ClientOut)
def update_client(client_id: int, update_data: ClientUpdate, db: Session = Depends(get_db)):
    client = db.query(models.Client).get(client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    if update_data.email and update_data.email != client.email:
        ensure_unique_email(db, update_data.email)

    if update_data.cpf and update_data.cpf != client.cpf:
        ensure_unique_cpf(db, update_data.cpf)

    for field, value in update_data.dict(exclude_unset=True).items():
        setattr(client, field, value)

    db.commit()
    db.refresh(client)
    return client


# Deleta um cliente
@router.delete("/{client_id}")
def delete_client(client_id: int, db: Session = Depends(get_db)):
    client = db.query(models.Client).get(client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    db.delete(client)
    db.commit()
    return {"detail": "Cliente deletado com sucesso"}
