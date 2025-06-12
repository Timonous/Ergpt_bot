from aiogram import Router, Bot, F
from aiogram.filters import CommandStart, Command, ChatMemberUpdatedFilter
from aiogram.types import ChatMemberUpdated, Message
from aiogram.enums import ChatType, ChatMemberStatus
from bot.auth import group_authorize_user

router = Router()



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

@router.message(Command("restart"), (F.chat.type.in_({ChatType.GROUP, ChatType.SUPERGROUP} & (~F.is_topic_message))))
async def group_restart_handler(message: Message) -> None:
    if not await group_authorize_user(message):
        return
    await message.answer("Пока не работает")
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
    await message.answer("Пока не подключен к ergpt")
    tg_user_id = str(message.from_user.id)
    #Тут нужно расписать логику отправки и получения запросов