from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.schemas.client_schema import ClientCreate, ClientOut, ClientUpdate
from app.db.database import get_db
from app.routes.auth_route import get_current_user, require_admin
from app.services.client_service import (
    get_clients as service_get_clients,
    get_client_by_id,
    create_client as service_create_client,
    update_client as service_update_client,
    delete_client as service_delete_client,
)

router = APIRouter(prefix="/clients", tags=["clients"])


@router.get("/", response_model=List[ClientOut])
def get_clients(
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
    skip: int = 0,
    limit: int = 10,
    name: Optional[str] = Query(None),
    email: Optional[str] = Query(None),
):
    return service_get_clients(db, skip, limit, name, email)


@router.post("/", response_model=ClientOut)
def create_client(
    client: ClientCreate,
    db: Session = Depends(get_db),
    user=Depends(require_admin),
):
    return service_create_client(db, client)


@router.get("/{client_id}", response_model=ClientOut)
def get_client(
    client_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)
):
    client = get_client_by_id(db, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return client


@router.put("/{client_id}", response_model=ClientOut)
def update_client(
    client_id: int,
    update_data: ClientUpdate,
    db: Session = Depends(get_db),
    user=Depends(require_admin),
):
    client = service_update_client(db, client_id, update_data)
    if not client:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return client


@router.delete("/{client_id}")
def delete_client(
    client_id: int, db: Session = Depends(get_db), user=Depends(require_admin)
):
    success = service_delete_client(db, client_id)
    if not success:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return {"detail": "Cliente deletado com sucesso"}
