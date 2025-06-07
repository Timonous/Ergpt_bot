from abc import ABC, abstractmethod
from user_profile.core.domain.user import User

class UserRepository(ABC):
    @abstractmethod
    async def get_by_telegram_id(self, telegram_id: str) -> User | None:
        pass

    @abstractmethod
    async def verify_telegram_id(self, user_id: int, telegram_id: str) -> bool:
        pass

    @abstractmethod
    async def update_phone(self, user_id: int, new_phone: str) -> None:
        pass