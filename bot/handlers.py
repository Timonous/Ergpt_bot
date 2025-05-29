import asyncio
import re

from aiogram import Router, Bot
from aiogram.enums import ChatAction, ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from telegramify_markdown import markdownify
from telegramify_markdown.customize import get_runtime_config

from bot.api.deepseek import call_deepseek_api

markdown_symbol = get_runtime_config().markdown_symbol
markdown_symbol.head_level_1 = ""
markdown_symbol.head_level_2 = ""
markdown_symbol.head_level_3 = ""

router = Router()

def escape_markdown(text: str) -> str:
    escape_chars = r'\_*[]()~`>#+-=|{}.!'
    return re.sub(f'([{re.escape(escape_chars)}])', r'\\\1', text)

@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(
        f"👋 Привет, {message.from_user.first_name}! Добро пожаловать в DeepSeek Agent."
        f" Здесь ты можешь задавать любые вопросы, а я с радостью на них отвечу!"
    )

async def handle_deepseek(message: Message, bot: Bot):
    chat_id = message.chat.id
    text = message.text.strip()

    async def show_typing():
        while True:
            await bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)
            await asyncio.sleep(4)

    task = asyncio.create_task(show_typing())

    try:
        reply = await call_deepseek_api( text)
    except Exception as e:
        escaped_error = escape_markdown(str(e))
        await message.reply(f"Ошибка при обращении к DeepSeek: {escaped_error}")
        return
    finally:
        task.cancel()

    tg_md = markdownify(reply, max_line_length=None, normalize_whitespace=False)
    await message.reply(tg_md, parse_mode=ParseMode.MARKDOWN_V2)