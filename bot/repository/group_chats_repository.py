from db import get_db_pool


async def ensure_group_exists(group_id: int):
    db_pool = get_db_pool()
    chat_id = 1 # заглушка для корректности
    async with db_pool.acquire() as conn:
        await conn.execute(
            """
            INSERT INTO group_chats_erGPT (group_id, chat_id, created_at, updated_at, is_deleted)
            VALUES ($1, $2, NOW(), NOW(), FALSE)
            ON CONFLICT (group_id) DO NOTHING
            """,
            group_id, chat_id
        )

async def get_chat_for_group(group_id: int):
    db_pool = get_db_pool()
    async with db_pool.acquire() as conn:
        row = await conn.fetchrow(
            "SELECT chat_id FROM group_chats_erGPT WHERE group_id = $1",
            group_id
        )
        return row['chat_id'] if row else 1  # если чата нет, вернуть 1 как сигнал для создания

async def set_chat_for_group(group_id: int, chat_id: int):
    db_pool = get_db_pool()
    async with db_pool.acquire() as conn:
        await conn.execute(
            """
            INSERT INTO group_chats_erGPT (group_id, chat_id, created_at, updated_at, is_deleted)
            VALUES ($1, $2, NOW(), NOW(), FALSE)
            ON CONFLICT (group_id) DO UPDATE
            SET chat_id = EXCLUDED.chat_id,
                updated_at = NOW(),
                is_deleted = FALSE
            """,
            group_id, chat_id
        )

async def get_updateat_for_group(group_id: int):
    db_pool = get_db_pool()
    async with db_pool.acquire() as conn:
        row = await conn.fetchrow(
            "SELECT updated_at FROM group_chats_erGPT WHERE group_id = $1",
            group_id
        )
        return row['updated_at'] if row else None

async def set_updateat_for_chat(group_id: int):
    db_pool = get_db_pool()
    async with db_pool.acquire() as conn:
        await conn.execute(
            "UPDATE group_chats_erGPT SET updated_at = NOW() WHERE group_id = $1",
            group_id
        )

async def ensure_chat_deleted(group_id: int) -> bool:
    db_pool = get_db_pool()
    async with db_pool.acquire() as conn:
        result = await conn.fetchval(
            """
            SELECT is_deleted FROM group_chats_erGPT WHERE group_id = $1
            """,
            group_id
        )
        return result

async def set_chat_deleted(group_id: int):
    db_pool = get_db_pool()
    async with db_pool.acquire() as conn:
        await conn.execute(
            """
            UPDATE group_chats_erGPT SET is_deleted = TRUE WHERE group_id = $1
            """,
            group_id
        )

async def get_outdated_chats():
    db_pool = get_db_pool()
    async with db_pool.acquire() as conn:
        result = await conn.fetch(
            """
            SELECT group_id, chat_id
            FROM group_chats_erGPT
            WHERE
                is_deleted = false
                AND updated_at < NOW() - INTERVAL '24 hours'
            """
        )
        return result