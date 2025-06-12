from aiogram import Router, Bot, F
from aiogram.filters import CommandStart, Command, ChatMemberUpdatedFilter
from aiogram.types import ChatMemberUpdated, Message
from aiogram.enums import ChatType, ChatMemberStatus

router = Router()



@router.message(CommandStart(), F.chat.type.in_({ChatType.GROUP, ChatType.SUPERGROUP}))
async def group_start_handler(message: Message) -> None:
    await message.answer(
        f"👋 Привет! Я Ergpt бот, ваш умный помошник.\n"
        f"Задавайте вопросы, и я с радостью на них отвечу!"
    )