from redis.asyncio import from_url
import config


def singleton(class_):
    instances = {}

    def get_instance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return get_instance


@singleton
class Cache:
    def __init__(self):
        self._redis = from_url(config.CACHE_URL, decode_responses=True)

    async def get(self, key: str) -> str:
        return await self._redis.get(key)

    async def set(self, key: str, value: str):
        return await self._redis.set(key, value)


