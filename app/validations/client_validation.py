from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.client_model import Client


# Valida Email
def ensure_unique_email(db: Session, email: str):
    if db.query(Client).filter_by(email=email).first():
        raise HTTPException(status_code=400, detail="Email is already in use")


# Valida CPF
def ensure_unique_cpf(db: Session, cpf: str):
    if db.query(Client).filter_by(cpf=cpf).first():
        raise HTTPException(status_code=400, detail="CPF is already in use")
