from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models import models

# Valida Email
def ensure_unique_email(db: Session, email: str):
    if db.query(models.Client).filter_by(email=email).first():
        raise HTTPException(status_code=400, detail="Email já está em uso")

# Valida CPF
def ensure_unique_cpf(db: Session, cpf: str):
    if db.query(models.Client).filter_by(cpf=cpf).first():
        raise HTTPException(status_code=400, detail="CPF já está em uso")
