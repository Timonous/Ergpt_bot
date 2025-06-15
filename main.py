import asyncio
import logging
import sys
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand, BotCommandScopeAllPrivateChats, BotCommandScopeAllGroupChats

from bot.repository.commands_repository import init_default_commands
from db import create_pool, set_db_pool
from settings import config
from bot.handlers import router as main_router
from bot.group_handlers import router as group_router
from bot.auth import router as auth_router, daily_staff_status_check
from bot.api.ergpt import daily_chats_delete



async def set_bot_commands(bot: Bot):
    # Команды для всех приватных чатов
    await bot.set_my_commands(
        commands=[
            BotCommand(command="help", description="Справка по боту"),
            BotCommand(command="add", description="Добавить в группу"),
            BotCommand(command="restart", description="Перезапуск чата"),
            BotCommand(command="deepseek", description="Сделать запрос в deepseek"),
            BotCommand(command="support", description="Контакты тех поддержки"),
        ],
        scope=BotCommandScopeAllPrivateChats()
    )

    # Команды для всех групп
    await bot.set_my_commands(
        commands=[
            BotCommand(command="help", description="Информация о боте"),
            BotCommand(command="restart", description="Перезапуск чата"),
            BotCommand(command="support", description="Контакты тех поддержки"),
        ],
        scope=BotCommandScopeAllGroupChats()
    )


async def main() -> None:
    # Подключение к БД
    db_pool = await create_pool()
    set_db_pool(db_pool)
    await daily_chats_delete()

    bot = Bot(token=config.BOT_TOKEN)
    await set_bot_commands(bot)
    dp = Dispatcher()

    # Подключение роутеров
    dp.include_router(group_router)
    dp.include_router(auth_router)
    dp.include_router(main_router)

    #Настройка автозапуска функции
    scheduler = AsyncIOScheduler()
    scheduler.add_job(daily_staff_status_check, CronTrigger(hour=00, minute=00))
    scheduler.add_job(daily_chats_delete, CronTrigger(hour=2, minute=00))
    scheduler.start()

    #Можно удалить после перовго запуска
    await init_default_commands()

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