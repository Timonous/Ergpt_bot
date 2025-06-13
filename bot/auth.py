import logging

from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
import re

from bot.repository.staff_repository import get_is_employed_by_phone, get_staff_by_phone
from bot.repository.user_repository import get_user_info_by_tguser, get_active_users, update_users_is_active, \
    insert_new_user
from db import get_db_pool

router = Router()


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

async def get_auth_user_by_telegramid(telegram_id: int):
    db_pool = get_db_pool()
    async with db_pool.acquire() as conn:
        user = await get_user_info_by_tguser(telegram_id)
        return user

async def daily_staff_status_check():
    """
    Деактивирует пользователей, которые больше не работают в компании.
    Возвращает количество деактивированных пользователей.
    """
    db_pool = get_db_pool()
    async with db_pool.acquire() as conn:
        # Получаем всех активных пользователей
        users = await get_active_users()

        for user in users:
            phone = user['phone']
            # Проверяем сотрудника в таблице staff
            staff = await get_is_employed_by_phone(phone)

            # Если сотрудник не найден или уволен - деактивируем
            if not staff or not staff['is_employed']:
                await update_users_is_active(user)
                logging.info(f"Пользователь c telegram_id:({user['telegram_id']}) был деактивирован")


async def check_staff_authorization(phone: str):
    """
    Проверяет наличие телефона в таблице staff и статус isemployed.
    Возвращает (True, staff_id) при успехе или (False, причина).
    """
    db_pool = get_db_pool()
    normalized_phone = normalize_phone_number(phone)
    async with db_pool.acquire() as conn:
        staff = await get_staff_by_phone(normalized_phone)
        if not staff:
            return False, "😴 Извините, вы не являетесь сотрудником ЭР-Телеком"
        if staff.get("is_employed") is False:
            return False, "😴 К сожалению, вы больше не являетесь сотрудником ЭР-Телеком"
        return True, staff.get("id")

async def authorize_user(message: Message) -> bool:
    auth_user = await get_auth_user_by_telegramid(message.chat.id)
    if auth_user is not None:
        if not auth_user.get("is_active"):
            await message.answer(
                f"😴 Похоже вы больше не являетесь сотрудником ЭР-Телеком.\n\n"
                "❗️ Если произошла ошибка, обратитесь в тех поддержку /support.",
                reply_markup=ReplyKeyboardRemove()
            )
            return False
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

async def group_authorize_user(message: Message) -> bool:
    auth_user = await get_auth_user_by_telegramid(message.from_user.id)
    if auth_user is not None:
        if not auth_user.get("is_active"):
            await message.answer(
                f"😴 Похоже вы больше не являетесь сотрудником ЭР-Телеком.\n\n"
                "❗️ Если произошла ошибка, обратитесь в тех поддержку /support."
            )
            return False
        return True
    await message.answer(
        f"😴 Для использования моих функций необходимо быть авторизованным.\n"
        "Для регистрации перейдите в личный чат со мной @Ergpt_test_bot"
    )
    return False

@router.message(F.contact)
async def handle_contact(message: Message):
    contact = message.contact
    phone = contact.phone_number

    # Проверяем авторизацию по номеру
    authorized, result = await check_staff_authorization(phone)

    if not authorized:
        await message.answer(result, reply_markup=ReplyKeyboardRemove())
        return

    staff_id = result

    if await get_auth_user_by_telegramid(message.chat.id) is None:
        # Регистрируем пользователя
        db_pool = get_db_pool()
        async with db_pool.acquire() as conn:
            await insert_new_user(message, phone, staff_id)
        await message.answer(
            "✅ Спасибо! Регистрация прошла успешно.\n"
            "Задавай вопросы, и я с радостью на них отвечу!",
            reply_markup=ReplyKeyboardRemove()
        )
        return

    await message.answer(
        "Ты уже зарегистрирован👌\n"
        "Задавай вопросы, и я с радостью на них отвечу!",
        reply_markup=ReplyKeyboardRemove()
    )
