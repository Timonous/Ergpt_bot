from db import get_db_pool

async def get_userid_by_tguser(tguser_id: str):
    db_pool = get_db_pool()
    async with db_pool.acquire() as conn:
        row = await conn.fetchrow(
            "SELECT id FROM users WHERE telegram_id = $1",
            tguser_id
        )
        return row['id'] if row else None

async def get_user_info_by_tguser(telegram_id: str):
    db_pool = get_db_pool()
    async with db_pool.acquire() as conn:
        row = await conn.fetchrow(
            "SELECT * FROM users WHERE telegram_id = $1",
            str(telegram_id)
        )
        return row if row else None

async def get_active_users():
    db_pool = get_db_pool()
    async with db_pool.acquire() as conn:
        row = await conn.fetchrow(
            "SELECT * FROM users WHERE is_active = TRUE"
        )
        return row if row else None

async def update_users_is_active(user):
    db_pool = get_db_pool()
    async with db_pool.acquire() as conn:
        row = await conn.execute(
            "UPDATE users SET is_active = FALSE WHERE telegram_id = $1",
            user['telegram_id']
        )
        return row if row else None

async def insert_new_user(message, phone, staff_id):
    db_pool = get_db_pool()
    async with db_pool.acquire() as conn:
        row = await conn.execute(
            "INSERT INTO users (telegram_id, phone, staff_id) VALUES ($1, $2, $3)",
            str(message.chat.id), phone, staff_id
        )
        return row if row else None

async def get_all_admin_users():
    db_pool = get_db_pool()
    async with db_pool.acquire() as conn:
        admin_users = await conn.fetch(
            "SELECT * FROM users WHERE role_id = 1"
        )
        return admin_users
