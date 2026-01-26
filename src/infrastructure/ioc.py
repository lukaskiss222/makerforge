from collections.abc import AsyncIterable
from typing import Protocol

from dishka import AsyncContainer, Provider, Scope, make_async_container, provide
from redis.asyncio import Redis as AsyncRedis

from makerforge.settings import Settings

global_container: AsyncContainer | None = None


class CommonRedis(Protocol): ...


class RedisProvider(Provider):
    def __init__(self, settings: Settings):
        super().__init__()
        self._settings = settings

    @provide(provides=CommonRedis, scope=Scope.APP)
    async def processed_events_redis(self) -> AsyncIterable[AsyncRedis]:
        async with AsyncRedis(
            host=self._settings.redis_dsn.host,
        ) as redis:
            yield redis


class SettingsProvider(Provider):
    def __init__(self, settings: Settings):
        super().__init__()
        self.settings = settings

    @provide(scope=Scope.APP)
    def provide_settings(self) -> Settings:
        """Provides the current settings instance to the container."""
        return self.settings


def init_container(settings: Settings) -> AsyncContainer:
    global global_container
    container = make_async_container(RedisProvider(settings), SettingsProvider(settings))
    global_container = container
    return container


def get_container() -> AsyncContainer:
    if global_container is None:
        raise RuntimeError("Container is not initialized yet!")
    return global_container


__all__ = [
    "get_container",
    "init_container",
]
