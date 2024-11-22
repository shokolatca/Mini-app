import asyncio
import logging
from aiohttp import web
from my_bot.handlers import router
from my_bot.config import bot
from aiogram import Dispatcher
import os

logging.basicConfig(level=logging.INFO)

dp = Dispatcher()
dp.include_router(router)

routes = web.RouteTableDef()

@routes.get('/')
async def index(request):
    return web.FileResponse('./webapp/index.html')

app = web.Application()
app.add_routes(routes)
app.router.add_static('/static/', path='./webapp/static', name='static')

async def start_web_app():
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 8080)
    await site.start()
    logging.info("Web app started on http://0.0.0.0:8080")

async def main():
    logging.info("Starting bot and web app")
    await bot.delete_webhook(drop_pending_updates=True)
    
    await asyncio.gather(
        dp.start_polling(bot),
        start_web_app(),
    )

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.error("Bot stopped!")
