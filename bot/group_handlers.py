import re

from aiogram import Router, Bot, F
from aiogram.filters import CommandStart, Command, ChatMemberUpdatedFilter
from aiogram.types import ChatMemberUpdated, Message
from aiogram.enums import ChatType, ChatMemberStatus, ParseMode
from telegramify_markdown import markdownify

from bot.auth import group_authorize_user
from bot.handlers import limiter

from bot.repository.group_chats_repository import get_chat_for_group, set_chat_for_group, get_updateat_for_group, \
    set_updateat_for_chat, ensure_group_exists, ensure_chat_deleted, set_chat_deleted
from bot.api.ergpt import send_ergpt_message, create_ergpt_chat, delete_ergpt_chat


router = Router()

def escape_markdown(text: str) -> str:
    escape_chars = r'\_*[]()~`>#+-=|{}.!'
    return re.sub(f'([{re.escape(escape_chars)}])', r'\\\1', text)

@router.message(CommandStart(), F.chat.type.in_({ChatType.GROUP, ChatType.SUPERGROUP}))
async def group_start_handler(message: Message) -> None:
    await message.answer(
        f"👋 Привет! Я Ergpt бот, ваш умный помошник.\n"
        f"Напиши мое имя Ergpt или Эргпт со своим вопросом и я с радостью отвечу!"
    )

@router.message(Command("help"), F.chat.type.in_({ChatType.GROUP, ChatType.SUPERGROUP}))
async def group_help_handler(message: Message) -> None:
    help_text = (
        "ℹ️ *Справка по боту Ergpt*\n\n"
        "🤖 Бот отвечает при упоминании его в сообщении через 'Ergpt' или 'Эргпт', а так же при ответе на сообщения от Ergpt\n\n"
        "Доступные команды в групповом чате:\n"
        "/restart - Перезапуск чата\n"
        "/support - Контакты тех. поддержки\n\n"
        "❗ Бот доступен только авторизированным сотрудникам Эр-телеком.\n"
        "Для авторизации перейдите в личный чат @Ergpt_test_bot и пройдите регистрацию")
    await message.answer(help_text)

@router.message(
    Command("restart"),
    F.chat.type.in_({ChatType.GROUP, ChatType.SUPERGROUP} & (~F.is_topic_message)) # возможн оошибка со скобками
)
async def group_restart_handler(message: Message) -> None:
    if not await group_authorize_user(message):
        return
    group_id = message.chat.id
    ergpt_chat_id = await get_chat_for_group(group_id)
    text = "😴Упс, Что-то пошло не так...\nПопробуйте позже."
    if ergpt_chat_id is not None:
        response = await delete_ergpt_chat(ergpt_chat_id)
        if response is not None:
            await set_chat_deleted(group_id)
            text = (
                "😉Хорошо, начнем все с чистого листа\n"
                "Задавай вопрос, я с радостью на него отвечу!"
            )
    await message.answer(text)
    #Расписать логику отчистки чата если в групповом чате будет отдельный чат в ergpt

@router.message(
    (
        F.chat.type.in_({ChatType.GROUP, ChatType.SUPERGROUP})
        & (~F.is_topic_message)
        & (F.text.contains("Ergpt") | F.text.contains("Эргпт") | F.text.contains("ergpt") | F.text.contains("эргпт") | F.reply_to_message.from_user.id)
    )
)
async def group_handle_ergpt(message: Message, bot: Bot):
    if not await group_authorize_user(message):
        return
    group_id = message.chat.id
    #Тут нужно расписать логику отправки и получения запросов
    allowed = await limiter.is_allowed(group_id)
    if not allowed:
        await message.reply("⏳ Слишком много запросов. Попробуйте позже.")
        return

    global_allowed = await limiter.is_global_limit_allowed()
    if not global_allowed:
        await message.reply("⚠️ Сервер временно перегружен. Попробуйте позже.")
        return

    text = message.text.strip()

    await check_group(group_id)  # проверяем, что пользователь есть в базе данных чатов
    ergpt_chat_id = await get_chat_for_group(group_id)  # ищем чат для юзера
    if ergpt_chat_id == 1:  # если у пользователя ещё не было чата, создаем его
        ergpt_chat_id = await create_ergpt_chat_for_group(group_id)
    else:
        updated_at = await get_updated_at(group_id)
        if updated_at is not None and await is_deleted_chat_by_group(group_id):  # если чат был удален, создаем новый
            await delete_ergpt_chat(ergpt_chat_id)  # удаляем старый чат
            ergpt_chat_id = await create_ergpt_chat_for_group(group_id)
        else:  # иначе просто обновляем время последенго обращения
            await set_updated_at(group_id)
    try:
        reply = await send_ergpt_message(chat_id=ergpt_chat_id, msg=text)
        if reply is None:
            await message.reply("😴Упс, Что-то пошло не так...\nПопробуйте позже.")
            return
    except Exception as e:
        escaped_error = escape_markdown(str(e))
        await message.reply(f"Ошибка при обращении к ergpt: {escaped_error}")
        return

    tg_md = markdownify(reply, max_line_length=None, normalize_whitespace=False)
    await message.reply(tg_md, parse_mode=ParseMode.MARKDOWN_V2)

async def create_ergpt_chat_for_group(group_id: int):
    assistant_id = 14  # универсальный помошник
    ergpt_chat_id = await create_ergpt_chat(assistant_id)
    await set_chat_for_group(group_id, ergpt_chat_id)
    return ergpt_chat_id

async def get_updated_at(group_id):
    return await get_updateat_for_group(group_id)

async def set_updated_at(group_id):
    await set_updateat_for_chat(group_id)
    return True

async def check_group(group_id):
    await ensure_group_exists(group_id)
    return True

async def is_deleted_chat_by_group(group_id: int):
    return await ensure_chat_deleted(group_id)

async def delete_chat(group_id: int):
    await set_chat_deleted(group_id)