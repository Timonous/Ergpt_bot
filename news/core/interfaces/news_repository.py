from abc import ABC, abstractmethod
from news.core.domain.models import News, Staff, User
from typing import List, Optional

class NewsRepository(ABC):
    @abstractmethod
    async def get_all_with_authors(self, limit: int = 10, offset: int = 0) -> List[News]:
        pass

class StaffRepository(ABC):
    @abstractmethod
    async def get_by_id(self, staff_id: int) -> Optional[Staff]:
        pass

class UserRepository(ABC):
    @abstractmethod
    async def get_by_staff_id(self, staff_id: int) -> Optional[User]:
        pass