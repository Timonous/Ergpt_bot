# core/domain/models.py
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Staff:
    id: int
    name: str
    surname: str
    phone: str
    is_employed: bool

@dataclass
class User:
    id: int
    phone: str
    telegram_id: str
    role_id: int
    staff_id: int
    staff: Optional[Staff] = None

@dataclass
class News:
    id: int
    header: str
    text: str
    author_id: int
    likes: int
    created_at: datetime
    author: Optional[User] = None