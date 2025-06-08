
from infrastructure.db.repositories import (
    PostgreSQLNewsRepository,
    PostgreSQLStaffRepository,
    PostgreSQLUserRepository
)

async def get_news_repo(pool: Pool = Depends(get_db_pool)) -> NewsRepository:
    return PostgreSQLNewsRepository(pool)

async def get_news_use_cases(
    news_repo: NewsRepository = Depends(get_news_repo)
) -> NewsUseCases:
    return NewsUseCases(news_repo)