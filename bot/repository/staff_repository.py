from bot.auth import get_db_pool

async def get_is_employed_by_phone(phone: str):
    db_pool = get_db_pool()
    async with db_pool.acquire() as conn:
        row = await conn.fetchrow(
            "SELECT is_employed FROM staff WHERE phone = $1",
            phone
        )
        return row if row else None

async def get_staff_by_phone(phone: str):
    db_pool = get_db_pool()
    async with db_pool.acquire() as conn:
        row = await conn.fetchrow(
            "SELECT * FROM staff WHERE phone = $1",
            phone
        )
        return row if row else None
