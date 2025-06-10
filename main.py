import asyncio
import logging
import sys
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from aiogram import Bot, Dispatcher
from db import create_pool
from settings import config
from bot.handlers import router as deepseek_router
from bot.auth import router as auth_router, set_db_pool



async def daily_task():
    print("Выполняется ежедневная задача!")

async def main() -> None:
    #Настройка автозапуска функции
    scheduler = AsyncIOScheduler()
    scheduler.add_job(daily_task, CronTrigger(minute=10))
    scheduler.start()

    bot = Bot(token=config.BOT_TOKEN)
    dp = Dispatcher()

    # Подключение к БД
    db_pool = await create_pool()
    set_db_pool(db_pool)

    # Подключение роутеров
    dp.include_router(auth_router)
    dp.include_router(deepseek_router)

    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
            handlers=[
                logging.FileHandler("bot.log", encoding="utf-8"),
                logging.StreamHandler(sys.stdout)  # Чтобы логи продолжали отображаться в консоли
            ]
        )
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот отключен пользователем!")