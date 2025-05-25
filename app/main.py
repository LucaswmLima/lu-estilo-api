from fastapi import FastAPI
from app.db.database import engine, Base
from app.routes import auth_route
from app.routes import client_route
from app.routes import product_route

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth_route.router)
app.include_router(client_route.router)
app.include_router(product_route.router)
