import asyncio
import re
from aiogram import Router, Bot, F
from aiogram.enums import ChatAction, ParseMode, ChatType
from aiogram.filters import CommandStart
from aiogram.types import Message
from telegramify_markdown import markdownify
from telegramify_markdown.customize import get_runtime_config

from bot.RateLimiter import RateLimiter
from bot.api.deepseek import call_deepseek_api
from bot.api.ergpt import send_ergpt_message
from bot.auth import authorize_user

markdown_symbol = get_runtime_config().markdown_symbol
markdown_symbol.head_level_1 = ""
markdown_symbol.head_level_2 = ""
markdown_symbol.head_level_3 = ""

router = Router()

# Конфигурация рейт-лимита
MAX_REQUESTS = 1 # количество запросов от 1 человека
TIME_WINDOW = 5 # таймаут между запросами
REDIS_URL = "redis://localhost"  # URL Redis сервера
MAX_GLOBAL = 10 # максимум одновременных пользователей, которые могут сдлеать запрос

limiter = RateLimiter(max_requests = MAX_REQUESTS, window = TIME_WINDOW, redis_url = REDIS_URL, max_global = MAX_GLOBAL)

def escape_markdown(text: str) -> str:
    escape_chars = r'\_*[]()~`>#+-=|{}.!'
    return re.sub(f'([{re.escape(escape_chars)}])', r'\\\1', text)

@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(
        f"👋 Привет, {message.from_user.first_name}! Добро пожаловать в Ergpt bot.\n"
        f"Задавай вопросы, и я с радостью на них отвечу!"
    )

# @router.message(
#     (F.chat.type == ChatType.PRIVATE)
#     | F.text.contains("DeepSeek")  # можно заменить на username, если нужно
#     | (F.reply_to_message & F.reply_to_message.from_user)
# )
# async def handle_deepseek(message: Message, bot: Bot):
#     user_id = message.from_user.id
#
#     allowed = await limiter.is_allowed(user_id)
#     if not allowed:
#         await message.reply("⏳ Слишком много запросов. Попробуйте позже.")
#         return
#
#     global_allowed = await limiter.is_global_limit_allowed()
#     if not global_allowed:
#         await message.reply("⚠️ Сервер временно перегружен. Попробуйте позже.")
#         return
#
#     chat_id = message.chat.id
#     text = message.text.strip()
#     async def show_typing():
#         while True:
#             await bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)
#             await asyncio.sleep(4)
#
#     typing_task = asyncio.create_task(show_typing())
#     try:
#         reply = await call_deepseek_api(text)
#     except Exception as e:
#         escaped_error = escape_markdown(str(e))
#         await message.reply(f"Ошибка при обращении к DeepSeek: {escaped_error}")
#         return
#     finally:
#         typing_task.cancel()
#
#     tg_md = markdownify(reply, max_line_length=None, normalize_whitespace=False)
#     await message.reply(tg_md, parse_mode=ParseMode.MARKDOWN_V2)

@router.message(
    (F.chat.type == ChatType.PRIVATE)
    | F.text.contains("ergpt")  # можно заменить на username, если нужно
    | (F.reply_to_message & F.reply_to_message.from_user)
)
async def handle_ergpt(message: Message, bot: Bot):
    user_id = message.from_user.id

    allowed = await limiter.is_allowed(user_id)
    if not allowed:
        await message.reply("⏳ Слишком много запросов. Попробуйте позже.")
        return

    global_allowed = await limiter.is_global_limit_allowed()
    if not global_allowed:
        await message.reply("⚠️ Сервер временно перегружен. Попробуйте позже.")
        return

    chat_id = message.chat.id
    text = message.text.strip()
    async def show_typing():
        while True:
            await bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)
            await asyncio.sleep(4)

    typing_task = asyncio.create_task(show_typing())
    try:
        reply = await send_ergpt_message(chat_id = 82959, msg = text)
    except Exception as e:
        escaped_error = escape_markdown(str(e))
        await message.reply(f"Ошибка при обращении к DeepSeek: {escaped_error}")
        return
    finally:
        typing_task.cancel()

    tg_md = markdownify(reply, max_line_length=None, normalize_whitespace=False)
    await message.reply(tg_md, parse_mode=ParseMode.MARKDOWN_V2)
