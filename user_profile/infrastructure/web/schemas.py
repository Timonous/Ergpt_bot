from pydantic import BaseModel

class UserProfileResponse(BaseModel):
    name: str
    surname: str
    patronymic: str
    phone: str
    telegram_id: str
    vacancy: str
    email: str
