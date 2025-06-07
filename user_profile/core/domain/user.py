from dataclasses import dataclass
from user_profile.core.domain.staff import Staff

@dataclass
class User:
    id: int
    phone: str
    telegram_id: str
    role_id: int
    staff: Staff