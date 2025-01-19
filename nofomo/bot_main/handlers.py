# bot_main/handlers.py
import logging
from aiogram import Router, types, F
from bot_main.main import dp
from backend.db import AsyncSessionLocal
from backend.repository import UserRepository

logger = logging.getLogger(__name__)
router = Router()
dp.include_router(router)

@router.message(F.text == "/start")
async def cmd_start(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.username or message.from_user.first_name
    async with AsyncSessionLocal() as db:
        await UserRepository.upsert_user(db, user_id, username)

    await message.answer("Привет! Я бот. Можешь написать /products, чтобы увидеть список, или /myname.")

@router.message(F.text == "/myname")
async def cmd_myname(message: types.Message):
    user_id = message.from_user.id
    async with AsyncSessionLocal() as db:
        user = await UserRepository.get_user_by_tg_id(db, user_id)
    if user:
        await message.answer(f"Твоё имя: {user.username}")
    else:
        await message.answer("Я тебя не знаю. Используй /start, чтобы сохраниться.")
