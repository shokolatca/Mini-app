# backend/routers/auth.py
import os
import logging
from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import jwt
from backend.db import AsyncSessionLocal
from backend.repository import UserRepository

logger = logging.getLogger(__name__)
auth_router = APIRouter()

JWT_SECRET = os.getenv("JWT_SECRET", "jwtsecret")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_EXPIRE_MIN = int(os.getenv("JWT_EXPIRE_MINUTES", "60"))
REFRESH_EXPIRE_DAYS = 7

# In-memory хранение refresh-токенов (пример). В продакшене - в базе
refresh_storage = set()

class LoginRequest(BaseModel):
    telegram_id: int
    username: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str

class RefreshRequest(BaseModel):
    refresh_token: str

def create_token(data: dict, expires_in_minutes: int) -> str:
    expire = datetime.utcnow() + timedelta(minutes=expires_in_minutes)
    payload = data.copy()
    payload["exp"] = expire
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

@auth_router.post("/login", response_model=TokenResponse)
async def login_user(req: LoginRequest):
    async with AsyncSessionLocal() as db:
        user = await UserRepository.get_user_by_tg_id(db, req.telegram_id)
        if not user:
            # Создадим
            user = await UserRepository.upsert_user(db, req.telegram_id, req.username)

    access_payload = {"sub": "access", "user_id": user.id}
    refresh_payload = {"sub": "refresh", "user_id": user.id}

    access_token = create_token(access_payload, ACCESS_EXPIRE_MIN)
    refresh_token = create_token(refresh_payload, REFRESH_EXPIRE_DAYS * 24 * 60)

    refresh_storage.add(refresh_token)

    return TokenResponse(access_token=access_token, refresh_token=refresh_token)

@auth_router.post("/refresh", response_model=TokenResponse)
async def refresh_token(req: RefreshRequest):
    token = req.refresh_token
    if token not in refresh_storage:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        if payload.get("sub") != "refresh":
            raise HTTPException(status_code=401, detail="Not a refresh token")
        user_id = payload.get("user_id")
        if not user_id:
            raise HTTPException(status_code=401, detail="No user_id in token")

        # Создаём новые токены
        new_access_payload = {"sub": "access", "user_id": user_id}
        new_access_token = create_token(new_access_payload, ACCESS_EXPIRE_MIN)

        new_refresh_payload = {"sub": "refresh", "user_id": user_id}
        new_refresh_token = create_token(new_refresh_payload, REFRESH_EXPIRE_DAYS * 24 * 60)

        # Удаляем старый refresh, добавляем новый
        refresh_storage.discard(token)
        refresh_storage.add(new_refresh_token)

        return TokenResponse(access_token=new_access_token, refresh_token=new_refresh_token)

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Refresh token expired")
    except jwt.PyJWTError as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {e}")
