import redis.asyncio as redis
import json
import os

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

async def get_client():
    return redis.from_url(REDIS_URL, decode_responses=True)

async def get_cached(wallet: str) -> dict | None:
    client = await get_client()
    data = await client.get(f"openbcb:{wallet}")
    if data:
        return json.loads(data)
    return None

async def set_cached(wallet: str, result: dict, ttl: int = 3600) -> None:
    client = await get_client()
    await client.set(f"openbcb:{wallet}", json.dumps(result), ex=ttl)