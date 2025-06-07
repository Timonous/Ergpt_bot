from asyncpg import Pool
from user_profile.core.domain.staff import Staff
from user_profile.core.interfaces.staff_repository import StaffRepository


class PostgreSQLStaffRepository(StaffRepository):
    def __init__(self, pool: Pool):
        self.pool = pool

    async def get_by_id(self, staff_id: int) -> Staff | None:
        async with self.pool.acquire() as conn:
            record = await conn.fetchrow("""
                                            SELECT 
                                                id, 
                                                name, 
                                                surname, 
                                                patronymic, 
                                                phone, 
                                                isemployed, 
                                                email, 
                                                vacancy
                                            FROM staff 
                                            WHERE id = $1
                                         """, staff_id)

            if not record:
                return None

            staff = Staff(
                id=record['id'],
                name=record['name'],
                surname=record['surname'],
                phone=record['staff_phone'],
                is_employed=record['isemployed'],
                patronymic=record['patronymic'],
                vacancy=record['vacancy'],
                email=record['email']
            )

            return staff