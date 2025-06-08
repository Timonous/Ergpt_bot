from datetime import datetime

from pydantic import BaseModel

from user_profile.core.domain.user import User


class NewsResponse(BaseModel):
    id: int
    header: str
    text: str
    author: User
    createdAt: datetime
    likes: int
