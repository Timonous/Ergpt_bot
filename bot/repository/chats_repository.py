from bot.auth import get_db_pool


async def ensure_user_exists(user_id: int):
    db_pool = get_db_pool()
    chat_id = 1 # заглушка для корректности
    async with db_pool.acquire() as conn:
        await conn.execute(
            """
            INSERT INTO chats_ergpt (user_id, chat_id, created_at, updated_at, is_deleted)
            VALUES ($1, $2, NOW(), NOW(), FALSE)
            ON CONFLICT (user_id) DO NOTHING
            """,
            user_id, chat_id
        )

async def get_chat_for_user(user_id: int):
    db_pool = get_db_pool()
    async with db_pool.acquire() as conn:
        row = await conn.fetchrow(
            "SELECT chat_id FROM chats_ergpt WHERE user_id = $1",
            user_id
        )
        return row['chat_id'] if row else 1  # если чата нет, вернуть 1 как сигнал для создания

async def set_chat_for_user(user_id: int, chat_id: int):
    db_pool = get_db_pool()
    async with db_pool.acquire() as conn:
        await conn.execute(
            """
            INSERT INTO chats_ergpt (user_id, chat_id, created_at, updated_at, is_deleted)
            VALUES ($1, $2, NOW(), NOW(), FALSE)
            ON CONFLICT (user_id) DO UPDATE
            SET chat_id = EXCLUDED.chat_id,
                updated_at = NOW(),
                is_deleted = FALSE
            """,
            user_id, chat_id
        )

async def get_updateat_for_user(user_id: int):
    db_pool = get_db_pool()
    async with db_pool.acquire() as conn:
        row = await conn.fetchrow(
            "SELECT updated_at FROM chats_ergpt WHERE user_id = $1",
            user_id
        )
        return row['updated_at'] if row else None

async def set_updateat_for_chat(user_id: int):
    db_pool = get_db_pool()
    async with db_pool.acquire() as conn:
        await conn.execute(
            "UPDATE chats_ergpt SET updated_at = NOW() WHERE user_id = $1",
            user_id
        )

async def ensure_chat_deleted(user_id: int) -> bool:
    db_pool = get_db_pool()
    async with db_pool.acquire() as conn:
        result = await conn.fetchval(
            """
            SELECT is_deleted FROM chats_ergpt WHERE user_id = $1
            """,
            user_id
        )
        return result

async def set_chat_deleted(user_id: int):
    db_pool = get_db_pool()
    async with db_pool.acquire() as conn:
        await conn.execute(
            """
            UPDATE chats_ergpt SET is_deleted = TRUE WHERE user_id = $1
            """,
            user_id
        )

async def get_outdated_chats():
    db_pool = get_db_pool()
    async with db_pool.acquire() as conn:
        result = await conn.fetch(
            """
            SELECT user_id, chat_id
            FROM chats_ergpt
            WHERE
                is_deleted = false
                AND updated_at < NOW() - INTERVAL '24 hours'
            """
        )
        return result