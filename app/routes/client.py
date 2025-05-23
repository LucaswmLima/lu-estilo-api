from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.schemas.client import ClientCreate, ClientOut, ClientUpdate
from app.models import Client
from app.db.database import get_db
from app.validations.client import ensure_unique_email, ensure_unique_cpf
from app.routes.auth import get_current_user, require_admin

router = APIRouter(prefix="/clients", tags=["clients"])

# Listar todos os clientes (qualquer usuário logado pode)
@router.get("/", response_model=List[ClientOut])
def get_clients(
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
    skip: int = 0,
    limit: int = 10,
    name: Optional[str] = Query(None),
    email: Optional[str] = Query(None),
):
    query = db.query(Client)
    if name:
        query = query.filter(Client.name.contains(name))
    if email:
        query = query.filter(Client.email.contains(email))
    return query.offset(skip).limit(limit).all()


# Criar novo cliente (apenas admin)
@router.post("/", response_model=ClientOut)
def create_client(
    client: ClientCreate, db: Session = Depends(get_db), user=Depends(require_admin)
):
    ensure_unique_email(db, client.email)
    ensure_unique_cpf(db, client.cpf)

    db_client = Client(**client.dict())
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client


# Buscar cliente por ID (qualquer logado)
@router.get("/{client_id}", response_model=ClientOut)
def get_client(
    client_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)
):
    client = db.query(Client).get(client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return client


# Atualizar cliente (apenas admin)
@router.put("/{client_id}", response_model=ClientOut)
def update_client(
    client_id: int,
    update_data: ClientUpdate,
    db: Session = Depends(get_db),
    user=Depends(require_admin),
):
    client = db.query(Client).get(client_id)
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


# Deletar cliente (apenas admin)
@router.delete("/{client_id}")
def delete_client(
    client_id: int, db: Session = Depends(get_db), user=Depends(require_admin)
):
    client = db.query(Client).get(client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    db.delete(client)
    db.commit()
    return {"detail": "Cliente deletado com sucesso"}
