import json
import redis.asyncio as aioredis
from loguru import logger
from app.config import settings

redis_client = aioredis.from_url(settings.redis_url)


async def get_cached(key: str):
    data = await redis_client.get(key)
    if data:
        logger.info(f"Кеш знайдено: {key}")
        return json.loads(data)
    return None


async def set_cached(key: str, value, ttl: int = 3600):
    await redis_client.set(key, json.dumps(value), ex=ttl)
    logger.info(f"Збережено в кеш: {key} (TTL {ttl}с)")


async def delete_cached(key: str):
    await redis_client.delete(key)
    logger.info(f"Кеш видалено: {key}")