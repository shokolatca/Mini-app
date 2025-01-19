# backend/routers/webhook.py
import os
import logging
from fastapi import APIRouter, Request, HTTPException
from aiogram import types
from aiogram.exceptions import TelegramAPIError
from bot_main.main import dp, bot

logger = logging.getLogger(__name__)
webhook_router = APIRouter()

WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "secret")

@webhook_router.post("/{secret}")
async def telegram_webhook(secret: str, request: Request):
    if secret != WEBHOOK_SECRET:
        raise HTTPException(status_code=403, detail="Forbidden: wrong secret")

    try:
        data = await request.json()
        update = types.Update(**data)
    except Exception as e:
        logger.warning(f"Invalid update: {e}")
        raise HTTPException(status_code=400, detail="Invalid request body")

    await dp.process_update(update)
    return {"ok": True}

@webhook_router.get("/set_webhook")
async def set_webhook():
    domain = os.getenv("WEBHOOK_DOMAIN", "https://localhost")
    url = f"{domain}/tg/webhook/{WEBHOOK_SECRET}"
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await bot.set_webhook(url=url)
        return {"message": f"Webhook set to {url}"}
    except TelegramAPIError as e:
        raise HTTPException(status_code=500, detail=str(e))

@webhook_router.get("/delete_webhook")
async def delete_webhook():
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        return {"message": "Webhook deleted"}
    except TelegramAPIError as e:
        raise HTTPException(status_code=500, detail=str(e))
