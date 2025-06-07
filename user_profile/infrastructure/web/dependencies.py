from fastapi import Depends

from db import create_pool
from user_profile.core.interfaces.user_repository import UserRepository
from user_profile.infrastructure.db.user_repository_impl import PostgreSQLUserRepository

async def get_user_repo() -> UserRepository:
    pool = await create_pool()
    return PostgreSQLUserRepository(pool)