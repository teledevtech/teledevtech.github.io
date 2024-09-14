import asyncio
import datetime
from aiogram import Bot, Dispatcher
import user
import admin
from info import TOKEN


async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    dp.include_routers(user.router, admin.router)
    print("Бот запущен!", datetime.datetime.now().strftime("%d.%m.%Y %H:%M"))
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
