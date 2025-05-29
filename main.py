import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ChatType, ParseMode

from bot.handlers import handle_deepseek, router
from settings import config


async def main() -> None:
    bot = Bot(token=config.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN_V2))

    dp = Dispatcher()
    dp.include_router(router)

    username = (await bot.get_me()).username

    dp.message.register(
        handle_deepseek,
        (F.chat.type == ChatType.PRIVATE)
        | F.text.contains(username)
        | (F.reply_to_message & (F.reply_to_message.from_user.username == username))
    )

    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        logging.basicConfig(level=logging.INFO, stream=sys.stdout)
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот отключен пользователем!")