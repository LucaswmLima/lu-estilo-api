import os
from fastapi import APIRouter, FastAPI
import sentry_sdk
from app.db.database import engine, Base
from app.routes import auth_route, order_route, client_route, product_route

from dotenv import load_dotenv
load_dotenv()

sentry_sdk.init(
    dsn=os.getenv("SENTRY_DSN"),
    send_default_pii=True,
    traces_sample_rate=1.0
)


Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth_route.router)
app.include_router(client_route.router)
app.include_router(product_route.router)
app.include_router(order_route.router)



router_sentry = APIRouter(prefix="/sentry-error", tags=["sentry"])

@router_sentry.get("/debug")
async def trigger_error():
    division_by_zero = 1 / 0

app.include_router(router_sentry)
