from asyncpg import Pool
from user_profile.core.interfaces.user_repository import UserRepository
from user_profile.core.domain.user import User
from user_profile.core.domain.staff import Staff


class PostgreSQLUserRepository(UserRepository):
    def __init__(self, pool: Pool):
        self.pool = pool

    async def get_by_telegram_id(self, telegram_id: str) -> User | None:
        async with self.pool.acquire() as conn:
            record = await conn.fetchrow("""
                                         SELECT u.*, 
                                                s.name,
                                                s.surname,
                                                s.patronymic,
                                                s.phone as staff_phone,
                                                s.isEmployed,
                                                s.vacancy,
                                                s.email
                                         FROM users u
                                         JOIN staff s ON u.staffID = s.id
                                         WHERE u.telegramID = $1
                                         """, telegram_id)

            if not record:
                return None

            staff = Staff(
                id=record['staffid'],
                name=record['name'],
                surname=record['surname'],
                phone=record['staff_phone'],
                is_employed=record['isemployed'],
                patronymic=record['patronymic'],
                vacancy=record['vacancy'],
                email=record['email']
            )

            return User(
                id=record['id'],
                phone=record['phone'],
                telegram_id=record['telegramid'],
                role_id=record['roleid'],
                staff=staff
            )

    async def verify_telegram_id(self, user_id: int, telegram_id: str) -> bool:
        async with self.pool.acquire() as conn:
            db_telegram_id = await conn.fetchval(
                "SELECT telegramID FROM users WHERE id = $1",
                user_id
            )
            return db_telegram_id == telegram_id

    async def update_phone(self, user_id: int, new_phone: str) -> None:
        async with self.pool.acquire() as conn:
            await conn.execute(
                "UPDATE users SET phone = $1 WHERE id = $2",
                new_phone, user_id
            )