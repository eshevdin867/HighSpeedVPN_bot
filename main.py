import asyncio

from aiogram import Bot, Dispatcher

from config import BOT_TOKEN
from database.db import init_db
from handlers.start import router as start_router
from handlers.menu import router as menu_router
from handlers.support import router as support_router
from handlers.admin import router as admin_router
from handlers.purchase import router as purchase_router


bot = Bot(BOT_TOKEN)

dp = Dispatcher()


async def main():
    await init_db()

    dp.include_router(start_router)
    dp.include_router(menu_router)
    dp.include_router(purchase_router)
    dp.include_router(support_router)
    dp.include_router(admin_router)


    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
