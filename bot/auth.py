from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from asyncpg import Pool
import re

router = Router()
db_pool: Pool = None

def set_db_pool(pool: Pool):
    global db_pool
    db_pool = pool

def normalize_phone_number(raw_phone: str) -> str:
    # Удаляем все лишние символы
    digits = re.sub(r'\D', '', raw_phone)

    # Преобразуем 8xxxxxxxxxx → +7xxxxxxxxxx
    if digits.startswith('8') and len(digits) == 11:
        return '+7' + digits[1:]
    elif digits.startswith('7') and len(digits) == 11:
        return '+7' + digits[1:]
    elif digits.startswith('9') and len(digits) == 10:
        return '+7' + digits
    elif digits.startswith('7') and len(digits) == 10:
        return '+7' + digits[1:]
    elif digits.startswith('89') and len(digits) == 11:
        return '+7' + digits[1:]
    elif digits.startswith('79') and len(digits) == 11:
        return '+7' + digits[1:]
    elif digits.startswith('7') and len(digits) == 11:
        return '+7' + digits[1:]
    elif digits.startswith('') and len(digits) == 10:
        return '+7' + digits
    else:
        return '+' + digits  # на всякий случай

async def is_user_registered(telegram_id: int) -> bool:
    async with db_pool.acquire() as conn:
        user = await conn.fetchrow("SELECT * FROM users WHERE telegramid = $1", str(telegram_id))
        return user is not None

async def authorize_user(message: Message) -> bool:
    if await is_user_registered(message.chat.id):
        return True
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="📱 Отправить номер", request_contact=True)]],
        resize_keyboard=True
    )
    await message.answer(
    f"👋 Привет, {message.from_user.first_name}! Добро пожаловать в Ergpt bot.\n\n"
        "⭐Для получения доступа к моим функция необходимо зарегистрироваться.\n\n"
        "Пожалуйста, отправь свой номер телефона для регистрации👇",
        reply_markup=keyboard
    )
    return False

@router.message(F.contact)
async def handle_contact(message: Message):
    contact = message.contact
    raw_phone = contact.phone_number
    phone = normalize_phone_number(raw_phone)  # Нормализуем

    async with db_pool.acquire() as conn:
        # Поиск в таблице staff по номеру и проверка isemployed
        staff = await conn.fetchrow("SELECT * FROM staff WHERE phone = $1", phone)
        if not staff:
            await message.answer(
                "😴 Извините, вы не являетесь сотрудником ЭР-Телеком",
                reply_markup=ReplyKeyboardRemove()
            )
            return
        if staff.get("isemployed") is False:
            await message.answer(
                "😴 К сожалению, вы больше не работаете в ЭР-Телеком",
                reply_markup=ReplyKeyboardRemove()
            )
            return
        # Регистрируем пользователя
        await conn.execute("INSERT INTO users (telegramid, phone, staffid) VALUES ($1, $2, $3)", str(message.chat.id), phone, staff.get("id"))
    await message.answer(
        f"✅ Спасибо! Вы успешно зарегистрированы.\n"
            "Задавай вопросы, и я с радостью на них отвечу!",
            reply_markup=ReplyKeyboardRemove()
        )