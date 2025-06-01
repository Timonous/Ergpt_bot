from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from asyncpg import Pool

router = Router()
db_pool: Pool = None

def set_db_pool(pool: Pool):
    global db_pool
    db_pool = pool

async def is_user_registered(chat_id: int) -> bool:
    async with db_pool.acquire() as conn:
        user = await conn.fetchrow("SELECT * FROM users WHERE chat_id = $1", chat_id)
        return user is not None

async def authorize_user(message: Message) -> bool:
    if await is_user_registered(message.chat.id):
        return True
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="📱 Отправить номер", request_contact=True)]],
        resize_keyboard=True
    )
    await message.answer(
        "⛔️Для начала работы с ботом необходимо зарегистрироваться, пожалуйста разрешите использование вашего номера",
        reply_markup=keyboard
    )
    return False

@router.message(F.contact)
async def handle_contact(message: Message):
    contact = message.contact
    async with db_pool.acquire() as conn:
        await conn.execute(
            "INSERT INTO users (chat_id, phone) VALUES ($1, $2) ON CONFLICT DO NOTHING",
            message.chat.id, contact.phone_number
        )
    await message.answer("Спасибо! Вы успешно зарегистрированы ✅", reply_markup=ReplyKeyboardRemove())