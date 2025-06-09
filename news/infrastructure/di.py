from asyncpg import Pool
from fastapi import APIRouter, Depends
from news.core.interfaces.news_repository import NewsRepository
from news.core.usecases.news_case import NewsUseCases
from news.infrastructure.db.news_repository_impl import (
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