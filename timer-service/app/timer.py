import redis.asyncio as aioredis
from loguru import logger
from app.config import settings

redis_client = aioredis.from_url(settings.redis_url)


async def start_timer(user_id: str, game_id: str) -> None:
    key = f"timer:{user_id}:{game_id}"
    import time
    await redis_client.set(key, int(time.time()))
    logger.info(f"Таймер запущено: {key}")


async def get_elapsed_minutes(user_id: str, game_id: str) -> int:
    key = f"timer:{user_id}:{game_id}"
    import time
    start = await redis_client.get(key)
    if not start:
        return 0
    elapsed = int(time.time()) - int(start)
    return elapsed // 60


async def stop_timer(user_id: str, game_id: str) -> int:
    minutes = await get_elapsed_minutes(user_id, game_id)
    key = f"timer:{user_id}:{game_id}"
    await redis_client.delete(key)
    logger.info(f"Таймер зупинено: {key}, зіграно {minutes} хвилин")
    return minutes