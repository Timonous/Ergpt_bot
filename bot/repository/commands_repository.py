from db import get_db_pool

# Получить команду по коду
async def get_command_id_by_code(code: str) -> int | None:
    db_pool = get_db_pool()
    async with db_pool.acquire() as conn:
        row = await conn.fetchrow("SELECT id FROM commands WHERE code = $1", code)
        return row['id'] if row else None

# Инициализировать базовые команды (однократный вызов)
async def init_default_commands():
    db_pool = get_db_pool()
    async with db_pool.acquire() as conn:
        await conn.execute("""
            INSERT INTO commands (code, description)
            VALUES 
                ('ASK_QUESTION_ER', 'Задал вопрос в ergpt'),
                ('ASK_QUESTION_DS', 'Задал вопрос в deepseek'),
                ('RESTART_CHAT', 'Перезапустил чат')
            ON CONFLICT (code) DO NOTHING
        """)
