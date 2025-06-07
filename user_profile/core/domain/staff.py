from dataclasses import dataclass

@dataclass
class Staff:
    id: int
    name: str
    surname: str
    patronymic: str
    vacancy: str
    phone: str
    is_employed: bool
    email: str