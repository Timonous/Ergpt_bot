import asyncio
import re
from aiogram import Router, Bot, F
from aiogram.enums import ChatAction, ParseMode, ChatType
from aiogram.filters import CommandStart
from aiogram.types import Message
from telegramify_markdown import markdownify
from telegramify_markdown.customize import get_runtime_config
from bot.redis_bucket import RedisTokenBucket

from bot.api.deepseek import call_deepseek_api
from bot.auth import authorize_user

markdown_symbol = get_runtime_config().markdown_symbol
markdown_symbol.head_level_1 = ""
markdown_symbol.head_level_2 = ""
markdown_symbol.head_level_3 = ""

router = Router()

bucket = RedisTokenBucket(
    redis_url="redis://localhost:6379/0",
    bucket_key="gpt_api_tokens",
    max_tokens=10  # Количество одновременных запросов (размер ведра)
)

def escape_markdown(text: str) -> str:
    escape_chars = r'\_*[]()~`>#+-=|{}.!'
    return re.sub(f'([{re.escape(escape_chars)}])', r'\\\1', text)

@router.message(CommandStart())
async def command_start_handler(message: Message):
    if not await authorize_user(message):
        return
    await bucket.init_bucket()
    await message.answer(
        f"👋 Привет, {message.from_user.first_name}! Добро пожаловать в Ergpt bot.\n"
        f"Задавай вопросы, и я с радостью на них отвечу!"
    )

@router.message(
    (F.chat.type == ChatType.PRIVATE)
    | F.text.contains("DeepSeek")  # можно заменить на username, если нужно
    | (F.reply_to_message & F.reply_to_message.from_user)
)
async def handle_deepseek(message: Message, bot: Bot):
    if not await authorize_user(message):
        return

    chat_id = message.chat.id
    text = message.text.strip()

    async def show_typing():
        while True:
            await bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)
            await asyncio.sleep(4)

    typing_task = asyncio.create_task(show_typing())
    try:
        async with bucket.consume_token(message.from_user.id) as success:
            if success:
                reply = await call_deepseek_api(text)
            else:
                reply = "Сервер перегружен. Попробуйте позже."
    except Exception as e:
        escaped_error = escape_markdown(str(e))
        await message.reply(f"Ошибка при обращении к DeepSeek: {escaped_error}")
        return
    finally:
        typing_task.cancel()

    tg_md = markdownify(reply, max_line_length=None, normalize_whitespace=False)
    await message.reply(tg_md, parse_mode=ParseMode.MARKDOWN_V2)