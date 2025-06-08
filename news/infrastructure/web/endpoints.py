from fastapi import APIRouter, Depends

from user_profile.infrastructure.web.dependencies import get_user_repo
from user_profile.infrastructure.web.schemas import *
from user_profile.core.interfaces.user_repository import UserRepository

router = APIRouter(prefix="/webview")

@router.get("/news", response_model=UserProfileResponse)
async def get_profile(
    telegram_id: str,
    user_repo: UserRepository = Depends(get_user_repo)
):
    user = await user_repo.get_by_telegram_id(telegram_id)
    return {
        "name": user.staff.name,
        "surname": user.staff.surname,
        "patronymic": user.staff.patronymic,
        "phone": user.phone,
        "vacancy": user.staff.vacancy,
        "email": user.staff.email,
        "telegram_id": user.telegram_id
    }
