from typing import List

from news.core.domain.models import News
from news.core.interfaces.news_repository import NewsRepository
from asyncpg import Pool


class PostgreSQLNewsRepository(NewsRepository):
    def __init__(self, pool: Pool):
        self.pool = pool

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