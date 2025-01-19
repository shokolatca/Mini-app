# backend/server.py
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.routers.webhook import webhook_router
from backend.routers.api import api_router
from backend.routers.auth import auth_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Telegram Shop (No-Front)", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(webhook_router, prefix="/tg/webhook", tags=["webhook"])
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(api_router, prefix="/api", tags=["api"])

@app.get("/")
def root_index():
    return {"message": "Hello from Gunicorn+Uvicorn, no front in this build"}
