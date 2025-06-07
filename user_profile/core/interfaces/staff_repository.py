from abc import ABC, abstractmethod
from user_profile.core.domain.staff import Staff

class StaffRepository(ABC):
    @abstractmethod
    async def get_by_id(self, staff_id: int) -> Staff | None:
        pass