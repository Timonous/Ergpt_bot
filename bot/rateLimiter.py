import time
import redis.asyncio as redis

class rateLimiter:
    def __init__(self, max_requests: int, window: int, redis_url: str, max_global: int = 10):
        self.max_requests = max_requests
        self.window = window
        self.redis = redis.from_url(redis_url)
        self.max_global = max_global

    async def is_allowed(self, user_id: int) -> bool:
        now = time.time()
        key = f"rate_limit:{user_id}"
        # Удаляем устаревшие метки времени
        await self.redis.zremrangebyscore(key, 0, now - self.window)
        # Получаем текущее количество запросов
        count = await self.redis.zcard(key)
        if count >= self.max_requests:
            return False
        # Добавляем новый запрос
        await self.redis.zadd(key, {str(now): now})
        await self.redis.expire(key, self.window)
        return True

    async def is_global_limit_allowed(self, key: str = "global_rate_limit") -> bool:
        now = time.time()
        pipe = self.redis.pipeline()
        await pipe.zremrangebyscore(key, 0, now - self.window)
        await pipe.zadd(key, {str(now): now})
        await pipe.expire(key, self.window)
        await pipe.zcard(key)
        result = await pipe.execute()
        current_count = result[3]

        return current_count < self.max_global