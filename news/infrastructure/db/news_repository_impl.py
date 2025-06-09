from asyncpg import Pool
from news.core.domain.models import News, Staff, User
from news.core.interfaces.news_repository import NewsRepository, StaffRepository, UserRepository
from typing import List
from typing import Optional


class PostgreSQLNewsRepository(NewsRepository):
    def __init__(self, pool: Pool):
        self._pool = pool

    async def get_all_with_authors(self, limit: int = 10, offset: int = 0) -> List[News]:
        async with self._pool.acquire() as conn:
            return await conn.fetch("""
                                    SELECT n.id,
                                           n.header,
                                           n.text,
                                           n.authorID,
                                           n.likes,
                                           n.createdAt,
                                           s.name,
                                           s.surname
                                    FROM news n
                                             JOIN users u ON n.authorID = u.id
                                             JOIN staff s ON u.staffID = s.id
                                    ORDER BY n.createdAt DESC
                                    LIMIT $1 OFFSET $2
                                    """, limit, offset)

    def _record_to_news(self, record) -> News:
        staff = Staff(
            id=record['staff_id'],
            name=record['name'],
            surname=record['surname'],
            phone=record['staff_phone'],
            is_employed=record['isEmployed']
        )

        user = User(
            id=record['user_id'],
            phone=record['phone'],
            telegram_id=record['telegramID'],
            role_id=record['roleID'],
            staff_id=record['staffID'],
            staff=staff
        )

        return News(
            id=record['id'],
            header=record['header'],
            text=record['text'],
            author_id=record['authorID'],
            likes=record['likes'],
            created_at=record['createdAt'],
            author=user
        )


class PostgreSQLStaffRepository(StaffRepository):
    def __init__(self, pool: Pool):
        self._pool = pool

    async def get_by_id(self, staff_id: int) -> Optional[Staff]:
        async with self._pool.acquire() as conn:
            record = await conn.fetchrow(
                'SELECT * FROM staff WHERE id = $1',
                staff_id
            )
            return self._record_to_staff(record) if record else None

    def _record_to_staff(self, record) -> Staff:
        return Staff(
            id=record['id'],
            name=record['name'],
            surname=record['surname'],
            phone=record['phone'],
            is_employed=record['isEmployed']
        )

class PostgreSQLUserRepository(UserRepository):
    def __init__(self, pool: Pool):
        self._pool = pool

    async def get_by_id(self, user_id: int) -> Optional[User]:
        async with self._pool.acquire() as conn:
            record = await conn.fetchrow(
                'SELECT * FROM users WHERE id = $1',
                user_id
            )
            return self._record_to_user(record) if record else None

    async def get_by_telegram_id(self, telegram_id: str) -> Optional[User]:
        async with self._pool.acquire() as conn:
            record = await conn.fetchrow(
                'SELECT * FROM users WHERE telegramID = $1',
                telegram_id
            )
            return self._record_to_user(record) if record else None

    async def get_by_staff_id(self, staff_id: int) -> Optional[User]:
        async with self._pool.acquire() as conn:
            record = await conn.fetchrow(
                'SELECT * FROM users WHERE staffID = $1',
                staff_id
            )
            return self._record_to_user(record) if record else None

    def _record_to_user(self, record) -> User:
        return User(
            id=record['id'],
            phone=record['phone'],
            telegram_id=record['telegramID'],
            role_id=record['roleID'],
            staff_id=record['staffID']
        )