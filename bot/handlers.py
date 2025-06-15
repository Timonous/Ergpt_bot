import asyncio
import re
import os
from aiogram import Router, Bot, F
from aiogram.enums import ChatAction, ParseMode, ChatType
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, ChatMemberUpdated, CallbackQuery
from telegramify_markdown import markdownify
from telegramify_markdown.customize import get_runtime_config
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from bot.rate_limiter import rateLimiter
from bot.api.deepseek import call_deepseek_api
from bot.api.ergpt import send_ergpt_message, create_ergpt_chat, delete_ergpt_chat
from bot.auth import authorize_user
from bot.repository.chats_repository import get_chat_for_user, set_chat_for_user, get_updateat_for_user, \
    set_updateat_for_chat, ensure_user_exists, ensure_chat_deleted, set_chat_deleted
from bot.repository.user_repository import get_userid_by_tguser, get_all_admin_users
markdown_symbol = get_runtime_config().markdown_symbol
markdown_symbol.head_level_1 = ""
markdown_symbol.head_level_2 = ""
markdown_symbol.head_level_3 = ""

router = Router()

# Конфигурация рейт-лимита
MAX_REQUESTS = 1 # количество запросов от 1 человека
TIME_WINDOW = 5 # таймаут между запросами
REDIS_URL = os.getenv("REDIS_HOST")  # URL Redis сервера
MAX_GLOBAL = 10 # максимум одновременных пользователей, которые могут сдлеать запрос

limiter = rateLimiter(max_requests = MAX_REQUESTS, window = TIME_WINDOW, redis_url = REDIS_URL, max_global = MAX_GLOBAL)

def escape_markdown(text: str) -> str:
    escape_chars = r'\_*[]()~`>#+-=|{}.!'
    return re.sub(f'([{re.escape(escape_chars)}])', r'\\\1', text)

class DeepSeekStates(StatesGroup):
    # Класс состояний
    waiting_for_question = State()

class SupportStates(StatesGroup):
    waiting_for_message = State()
    waiting_for_admin_reply = State()



@router.message(CommandStart(), F.chat.type == ChatType.PRIVATE)
async def command_start_handler(message: Message) -> None:
    await message.answer(
        f"👋 Привет, {message.from_user.first_name}! Добро пожаловать в Ergpt bot.\n"
        f"Задавай вопросы, и я с радостью на них отвечу!"
    )

@router.message(Command("help"), F.chat.type == ChatType.PRIVATE)
async def command_help_handler(message: Message) -> None:
    help_text = (
        "ℹ️ *Справка по боту Ergpt*\n\n"
        "Доступные команды:\n"
        "/restart - Перезапуск чата\n"
        "/support - Контакты тех. поддержки\n"
        "/add - Добавить ergpt в беседу\n"
        "/deepseek - Сделать запрос в deepseek (авторизация не требуется)\n\n"
        "Вы можете выбрать сделать один запрос в deepseek, но со следующими ограничениями:\n"
        "* История чата не сохраняется\n"
        "* Добавить в беседу модель нельзя\n"
        "* Отсутствует возможность работы с файлами\n"
    )
    await message.answer(help_text)

@router.message(Command("support"))
async def command_support_handler(message: Message, state: FSMContext) -> None:
    await message.answer("✍ Напишите что у вас случилось, я отправил обращение в тех. поддержку")
    await state.set_state(SupportStates.waiting_for_message)

@router.message(SupportStates.waiting_for_message, F.chat.type == ChatType.PRIVATE)
async def handle_support_message(message: Message, bot: Bot, state: FSMContext):
    user_id = message.from_user.id
    message_text = f"❗ Вам пришло обращение от пользователя @{message.chat.username}:\n\n {message.text}"
    admin_users = await get_all_admin_users()
    if admin_users:
        reply_keyboard = InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text="📨 Ответить", callback_data=f"reply_to_user_{user_id}")]]
        )
        for admin in admin_users:
            await bot.send_message(admin['telegram_id'], message_text, reply_markup=reply_keyboard )
    await message.answer("👌 Спасибо, обращение было отправлено!")
    await state.clear()

@router.callback_query(F.data.startswith("reply_to_user_"))
async def handle_reply_button(callback: CallbackQuery, bot: Bot, state: FSMContext):
    user_id = int(callback.data.split("_")[-1])
    await state.update_data(target_user_id=user_id)
    await callback.message.answer("✍️ Введите ответ пользователю")
    await state.set_state(SupportStates.waiting_for_admin_reply)
    await callback.answer()

@router.message(SupportStates.waiting_for_admin_reply, F.chat.type == ChatType.PRIVATE)
async def handle_admin_reply(message: Message, bot: Bot, state: FSMContext):
    data = await state.get_data()
    target_user_id = data.get("target_user_id")
    if not target_user_id:
        await message.answer("❌ Ошибка: не найден получатель.")
        return
    try:
        await bot.send_message(
            target_user_id,
            f"📩 Ответ от поддержки:\n\n{message.text}"
        )
        await message.answer("✅ Ответ отправлен!")
    except Exception as e:
        await message.answer(f"❌ Не удалось отправить ответ: {e}")

    await state.clear()

@router.message(Command("add"), F.chat.type == ChatType.PRIVATE)
async def command_add_handler(message: Message) -> None:
    if not await authorize_user(message):
        return
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text="Добавить в групповой чат 👇",
                url="https://t.me/Ergpt_test_bot?startgroup=start"
            )]
        ]
    )
    await message.answer("😇 Добавьте меня в групповой чат — я очень полезный!", reply_markup=keyboard)

@router.message(Command("deepseek"), F.chat.type == ChatType.PRIVATE)
async def command_change_handler(message: Message, state: FSMContext) -> None:
    await message.answer("✍ Напишите ваш вопрос, отправлю ответ от deepseek")
    await state.set_state(DeepSeekStates.waiting_for_question)

@router.message(Command("restart"), F.chat.type == ChatType.PRIVATE)
async def command_restart_handler(message: Message) -> None:
    if not await authorize_user(message):
        return
    user_id = await get_user(str(message.chat.id))
    ergpt_chat_id = await get_chat_for_user(user_id)
    text = "😴Упс, Что-то пошло не так...\nПопробуйте позже."
    if ergpt_chat_id is not None:
        response = await delete_ergpt_chat(ergpt_chat_id)
        if response is not None:
            await set_chat_deleted(user_id)
            text = (
                "😉Хорошо, начнем все с чистого листа\n"
                "Задавай вопрос, я с радостью на него отвечу!"
            )
    await message.answer(text)

@router.message(DeepSeekStates.waiting_for_question, F.chat.type == ChatType.PRIVATE)
async def handle_deepseek(message: Message, bot: Bot, state: FSMContext):
    user_id = message.from_user.id

    allowed = await limiter.is_allowed(user_id)
    if not allowed:
        await message.reply("⏳ Слишком много запросов. Попробуйте позже.")
        await state.clear()
        return

    global_allowed = await limiter.is_global_limit_allowed()
    if not global_allowed:
        await message.reply("⚠️ Сервер временно перегружен. Попробуйте позже.")
        await state.clear()
        return

    chat_id = message.chat.id
    text = message.text.strip()

    async def show_typing():
        while True:
            await bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)
            await asyncio.sleep(4)

    typing_task = asyncio.create_task(show_typing())
    try:
        reply = await call_deepseek_api(text)
    except Exception as e:
        escaped_error = escape_markdown(str(e))
        await message.reply(f"Ошибка при обращении к DeepSeek: {escaped_error}")
        return
    finally:
        typing_task.cancel()
        await state.clear()

    tg_md = markdownify(reply, max_line_length=None, normalize_whitespace=False)
    await message.reply(tg_md, parse_mode=ParseMode.MARKDOWN_V2)
    await message.answer("😌 Если хотите ещё что-то спросить у deepseek напишите /deepseek повторно.")


@router.message(F.chat.type == ChatType.PRIVATE)
async def handle_ergpt(message: Message, bot: Bot):
    if not await authorize_user(message):
        return
    tguser_id = message.from_user.id

    allowed = await limiter.is_allowed(tguser_id)
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

    user_id = await get_user(str(tguser_id)) # находим id нашего юзероа по тг id
    await check_user(user_id) # проверяем, что пользователь есть в базе данных чатов
    ergpt_chat_id = await get_chat_for_user(user_id) # ищем чат для юзера
    if ergpt_chat_id == 1: # если у пользователя ещё не было чата, создаем его
        ergpt_chat_id = await create_ergpt_chat_for_user(user_id)
    else:
        updated_at = await get_updated_at(user_id)
        if updated_at is not None and await is_deleted_chat_by_user(user_id): # если чат был удален, создаем новый
            await delete_ergpt_chat(ergpt_chat_id) # удаляем старый чат
            ergpt_chat_id = await create_ergpt_chat_for_user(user_id)
        else: #иначе просто обновляем время последенго обращения
            await set_updated_at(user_id)
    try:
        reply = await send_ergpt_message(chat_id = ergpt_chat_id, msg = text)
        if reply is None:
            await message.reply("😴Упс, Что-то пошло не так...\nПопробуйте позже.")
            return
    except Exception as e:
        escaped_error = escape_markdown(str(e))
        await message.reply(f"Ошибка при обращении к ergpt: {escaped_error}")
        return
    finally:
        typing_task.cancel()

    tg_md = markdownify(reply, max_line_length=None, normalize_whitespace=False)
    await message.reply(tg_md, parse_mode=ParseMode.MARKDOWN_V2)

async def create_ergpt_chat_for_user(user_id: int):
    assistant_id = 14  # универсальный помошник
    ergpt_chat_id = await create_ergpt_chat(assistant_id)
    await set_chat_for_user(user_id, ergpt_chat_id)
    return ergpt_chat_id

async def get_updated_at(user_id):
    return await get_updateat_for_user(user_id)

async def set_updated_at(user_id):
    await set_updateat_for_chat(user_id)
    return True

async def get_user(tguser_id):
    return await get_userid_by_tguser(tguser_id)

async def check_user(user_id):
    await ensure_user_exists(user_id)
    return True
async def is_deleted_chat_by_user(user_id: int):
    return await ensure_chat_deleted(user_id)

async def delete_chat(user_id: int):
    await set_chat_deleted(user_id)
