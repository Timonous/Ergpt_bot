from db import get_db_pool
async def save_new_log(user_id, command_id: int):
    db_pool = get_db_pool()
    async with db_pool.acquire() as conn:
        await conn.execute(
            """
            INSERT INTO logs (user_id, command_id, created_at)
            VALUES ($1, $2, NOW())
            """,
            user_id, command_id
        )