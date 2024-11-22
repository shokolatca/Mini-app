from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
from aiogram.filters import CommandStart
import os

router = Router()

def web_app_keyboard(web_app_url):
    button = KeyboardButton(
        text="Открыть Web App",
        web_app=WebAppInfo(url=web_app_url)
    )
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[button]],
        resize_keyboard=True
    )
    return keyboard

@router.message(CommandStart())
async def send_welcome(message: Message):
    web_app_url = os.getenv('WEBAPP_URL')
    if not web_app_url:
        await message.answer("Ошибка: WEBAPP_URL не задан.")
        return
    await message.answer(
        "Привет! Нажми на кнопку ниже, чтобы открыть Web App.",
        reply_markup=web_app_keyboard(web_app_url)
    )

@router.message(F.web_app_data)
async def web_app_data_handler(message: Message):
    data = message.web_app_data.data
    await message.answer(f"Получены данные из Web App: {data}")
