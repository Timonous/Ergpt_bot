import redis
import contextlib
from typing import AsyncIterator

class RedisTokenBucket:
    def __init__(self, redis_url: str, bucket_key: str, max_tokens: int):
        self.redis = redis.from_url(redis_url)
        self.bucket_key = bucket_key
        self.max_tokens = max_tokens

    async def init_bucket(self) -> None:
        await self.redis.set(self.bucket_key, self.max_tokens)

    @contextlib.asynccontextmanager
    async def consume_token(self) -> AsyncIterator[bool]:
        token_acquired = False
        try:
            while True:
                await self.redis.watch(self.bucket_key)
                current_tokens = int(await self.redis.get(self.bucket_key) or 0)

                if current_tokens > 0:
                    pipeline = self.redis.pipeline()
                    pipeline.decr(self.bucket_key)
                    if await pipeline.execute():
                        token_acquired = True
                        break
                else: # Нет свободного токена, ставим в очередь
                    await self.redis.unwatch()
                    yield False
                    return

            yield True  # Токен получен

        finally:
            if token_acquired:
                await self.redis.incr(self.bucket_key)