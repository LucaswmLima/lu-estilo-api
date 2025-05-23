from fastapi import FastAPI
from app.db.database import engine, Base
from app.routes import auth
from app.routes import client
from app.routes import product

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router)
app.include_router(client.router)
app.include_router(product.router)
