import os
from aiogram import Bot
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv('API_TOKEN')

if not API_TOKEN:
    print("Error: API_TOKEN is not provided.")
    exit(1)
bot = Bot(token=API_TOKEN)
