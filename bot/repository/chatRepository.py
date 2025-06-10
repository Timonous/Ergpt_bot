from bot.auth import get_db_pool


async def ensure_user_exists(user_id: int):
    db_pool = get_db_pool()
    chat_id = 1 # заглушка для корректности
    async with db_pool.acquire() as conn:
        await conn.execute(
            """
            INSERT INTO chats_ergpt (userid, chatid, createdat, updatedat, isdeleted)
            VALUES ($1, $2, NOW(), NOW(), FALSE)
            ON CONFLICT (userid) DO NOTHING
            """,
            user_id, chat_id
        )

async def get_chat_for_user(user_id: int):
    db_pool = get_db_pool()
    async with db_pool.acquire() as conn:
        row = await conn.fetchrow(
            "SELECT chatid FROM chats_ergpt WHERE userid = $1",
            user_id
        )
        return row['chatid'] if row else 1  # если чата нет, вернуть 1 как сигнал для создания

async def set_chat_for_user(user_id: int, chat_id: int):
    db_pool = get_db_pool()
    async with db_pool.acquire() as conn:
        await conn.execute(
            """
            INSERT INTO chats_ergpt (userid, chatid, createdat, updatedat, isdeleted)
            VALUES ($1, $2, NOW(), NOW(), FALSE)
            ON CONFLICT (userid) DO UPDATE
            SET chatid = EXCLUDED.chatid,
                updatedat = NOW(),
                isdeleted = FALSE
            """,
            user_id, chat_id
        )

async def get_updateat_for_user(user_id: int):
    db_pool = get_db_pool()
    async with db_pool.acquire() as conn:
        row = await conn.fetchrow(
            "SELECT updatedat FROM chats_ergpt WHERE userid = $1",
            user_id
        )
        return row['updatedat'] if row else None

async def set_updateat_for_chat(user_id: int):
    db_pool = get_db_pool()
    async with db_pool.acquire() as conn:
        await conn.execute(
            "UPDATE chats_ergpt SET updatedat = NOW() WHERE userid = $1",
            user_id
        )

async def get_userid_by_tguser(tguser_id: str):
    db_pool = get_db_pool()
    async with db_pool.acquire() as conn:
        row = await conn.fetchrow(
            "SELECT id FROM users WHERE telegramid = $1",
            tguser_id
        )
        return row['id'] if row else None

async def ensure_chat_deleted(user_id: int) -> bool:
    db_pool = get_db_pool()
    async with db_pool.acquire() as conn:
        result = await conn.fetchval(
            """
            SELECT isdeleted FROM chats_ergpt WHERE userid = $1
            """,
            user_id
        )
        return result

async def set_chat_deleted(user_id: int):
    db_pool = get_db_pool()
    async with db_pool.acquire() as conn:
        await conn.execute(
            """
            UPDATE chats_ergpt SET isdeleted = TRUE WHERE userid = $1
            """,
            user_id
        )