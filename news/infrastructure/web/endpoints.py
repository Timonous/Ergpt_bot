from fastapi import APIRouter, Depends
from news.core.domain.models import News
from news.core.usecases.news_case import NewsUseCases
from typing import List

from news.infrastructure.di import get_news_use_cases

router = APIRouter(prefix="/webview")

@router.get("/news", response_model=List[News])
async def get_news_with_authors(
    limit: int = 10,
    offset: int = 0,
    use_case: NewsUseCases = Depends(get_news_use_cases)
):
    return await use_case.get_news_with_authors(limit, offset)
