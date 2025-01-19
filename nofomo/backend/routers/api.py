# backend/routers/api.py
import os
import logging
from fastapi import APIRouter, HTTPException, Depends, Header
from pydantic import BaseModel
from aiogram.exceptions import TelegramAPIError
from bot_main.main import bot
from backend.db import AsyncSessionLocal
from backend.repository import (UserRepository, ProductRepository, OrderRepository)
import jwt

logger = logging.getLogger(__name__)
api_router = APIRouter()

def decode_access_token(authorization: str = Header(...)) -> dict:
    """
    Пример "middleware"-зависимости для проверки access-токена.
    Authorization: Bearer <access_token>
    """
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="No Bearer token")
    token = authorization.split(" ")[1]

    # Декодируем
    from backend.routers.auth import JWT_SECRET, JWT_ALGORITHM
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        if payload.get("sub") != "access":
            raise HTTPException(status_code=401, detail="Not an access token")
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Access token expired")
    except jwt.PyJWTError as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {e}")

# ----------- Endpoints

@api_router.get("/products")
async def list_products():
    async with AsyncSessionLocal() as db:
        products = await ProductRepository.list_products(db)
    return [
        {
            "id": p.id,
            "name": p.name,
            "description": p.description,
            "file_path": p.file_path
        }
        for p in products
    ]

class BuyRequest(BaseModel):
    product_id: int

@api_router.post("/buy")
async def buy_product(
    req: BuyRequest,
    token_payload: dict = Depends(decode_access_token)
):
    """
    Создаёт заказ (created -> paid) и отправляет файл в чат.
    token_payload хранит {"user_id": ...}.
    """
    user_id = token_payload.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="No user_id in token")

    # Находим user, product, создаём order
    async with AsyncSessionLocal() as db:
        # Допустим user_id из токена = PK пользователя (не telegram_id).
        order = await OrderRepository.create_order(db, user_id, req.product_id)
        paid_order = await OrderRepository.update_order_status(db, order.id, "paid")

        # Находим product (нужно получить file_path)
        product = await ProductRepository.get_product_by_id(db, req.product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        # Находим user (telegram_id) — нам нужно chat_id
        # user_id = PK, нужно UserRepository.get_user_by_id (нужно дописать?)
        # или query. Упростим: user_id == telegram_id? Нет, тогда пишем новый метод:
        user = await db.get(UserRepository.model, user_id)  # model -> User
        if not user:
            raise HTTPException(status_code=404, detail="User not found in DB?")

    # Отправляем файл
    if not product.file_path:
        raise HTTPException(status_code=404, detail="No file path in product")
    chat_id = user.telegram_id

    import os
    full_path = os.path.join("/app/files", product.file_path)
    if not os.path.exists(full_path):
        raise HTTPException(status_code=404, detail="File not found on server")

    try:
        with open(full_path, "rb") as f:
            await bot.send_document(
                chat_id=chat_id,
                document=f,
                caption=f"Спасибо за покупку: {product.name}"
            )
    except TelegramAPIError as e:
        raise HTTPException(status_code=500, detail=f"Cannot send file: {e}")

    return {"order_id": paid_order.id, "status": "paid", "message": "file sent"}
