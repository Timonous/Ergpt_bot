import asyncpg
from asyncpg import Pool
from settings import config

# Функция создаёт пул подключений к PostgreSQL
async def create_pool():
    return await asyncpg.create_pool(
        user=config.DB_USER,
        password=config.DB_PASSWORD,
        database=config.DB_NAME,
        host=config.DB_HOST,
        port=config.DB_PORT
    )

db_pool: Pool = None

def set_db_pool(pool: Pool):
    global db_pool
    db_pool = pool

def get_db_pool():
    return db_pool