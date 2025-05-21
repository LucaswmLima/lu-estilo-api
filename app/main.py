from fastapi import FastAPI
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("App is starting up...")
    
    yield
    
    print("App is shutting down...")

app = FastAPI(lifespan=lifespan)
