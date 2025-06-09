from news.core.domain.models import News
from news.core.interfaces.news_repository import NewsRepository
from typing import List

class NewsUseCases:
    def __init__(self, news_repo: NewsRepository):
        self._news_repo = news_repo

    async def get_news_with_authors(self, limit: int = 10, offset: int = 0) -> List[News]:
        return await self._news_repo.get_all_with_authors(limit, offset)